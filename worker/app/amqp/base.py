from worker.app.config import app_config
from app.amqp.async_timed_iterable import AsyncTimedIterable
from typing import Any, Callable
import asyncio
import aio_pika
import logging
logging.getLogger('aiormq').propagate = False
logging.getLogger('aio_pika').propagate = False


class RabbitMqHandlerBase(object):
    """
    Base class, used for implementation RPC over RabbitMQ
    """
    __connection = None
    __channel = None

    @classmethod
    async def get_channel(cls) -> aio_pika.channel.Channel:
        """
        Get RabbitMQ connection channel. Connection and channel are persistent, stored into class fields.
        Returns:
            Channel
        """
        loop = asyncio.get_event_loop()
        if cls.__connection is None:
            cls.__connection = await aio_pika.connect_robust(
                app_config.amqp_cs, loop=loop
            )
        if cls.__channel is not None and cls.__channel.is_closed:
            del cls.__channel
        if cls.__channel is None:
            cls.__channel = await cls.__connection.channel()
        return cls.__channel

    def __del__(self) -> None:
        """
        Delete class instance, and correctly close connection.
        """
        if self.__connection is not None:
            self.__connection.close()

    @classmethod
    async def disconnect(cls):
        if cls.__channel is not None:
            await cls.__channel.close()
        if cls.__connection is not None:
            await cls.__connection.close()
        cls.__connection = None
        cls.__channel = None

    @classmethod
    async def listen(cls):
        pass

    @classmethod
    async def basic_send(cls, queue_name: str, payload: bytes, reply_to: str = None, correlation_id: str = None, ttl: int = None) -> None:
        """
        Basic send method, used to send request for executor trough RabbitMQ queue.

        Args:
            queue_name (str): name of the queue, used as a routing key
            payload(bytes): message
            reply_to(str): result queue
            correlation_id(str): same as request_id
            ttl(int): TTL in seconds
        Returns:
            None
        """
        channel = await cls.get_channel()
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=payload,
                reply_to=reply_to,
                correlation_id=correlation_id,
                expiration=ttl
            ),
            routing_key=queue_name
        )

    @classmethod
    async def basic_receive(cls, queue_name: str,
                            timeout: float = None,
                            parser_callback: Callable = None,
                            exclusive_queue: bool = False,
                            delete_queue: bool = False) -> Any:
        """
        Basic receive method, used to await and get message from specific queue.
        Args:
            queue_name(str): queue to listen
            timeout(float): timeout, applied between chunks arrival, None means no timeout
            parser_callback(Callable): callback function, used to preprocess message, and returns a tuple (Any, bool), bool value means 'continue processing' or not
            exclusive_queue(bool): is the queue exclusive (lives only while connection alive)
            delete_queue(bool): delete queue after processing
        Returns:
            Any: result of message processing by callback or raw message bytes
        """
        channel = await cls.get_channel()
        queue = await channel.declare_queue(queue_name, exclusive=exclusive_queue)
        try:
            async with queue.iterator() as queue_iter:
                iter_wrapper = AsyncTimedIterable(queue_iter, timeout, parser_callback)
                async for message in iter_wrapper:
                    yield message
        except Exception as e:
            raise e
        finally:
            if delete_queue:
                await queue.delete(if_unused=False, if_empty=False)
