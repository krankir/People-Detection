from __future__ import annotations

import asyncio
import json
import uuid
from typing import Any, Generator, Tuple
import traceback
import aio_pika
from src.context import request_id
from src.amqp.base import RabbitMqHandlerBase
from src.logger import logger

from src.amqp.request_dispatcher import RequestDispatcher


class ServiceHandler(RabbitMqHandlerBase):
    __worker_tasks_queue = 'service_1'
    __instance_listen_queue = f'{__worker_tasks_queue}_results'

    @classmethod
    async def listen(cls):
        try:
            logger.info('Starting ServiceHandler listener {}'.format(cls.__instance_listen_queue))

            def parse_result(incoming_message: aio_pika.Message) -> Tuple[Any, bool]:
                message = json.loads(incoming_message.body.decode('utf-8'))
                logger.debug(f"New message {message}")
                RequestDispatcher.set_result(incoming_message.correlation_id, message)
                return message, True

            async for _ in cls.basic_receive(cls.__instance_listen_queue,
                                             parser_callback=parse_result,
                                             exclusive_queue=True):
                pass
        except Exception as e:
            logger.exception(e)
            traceback.print_tb(e.__traceback__)

    @classmethod
    async def call_service(cls) -> Any:
        data = json.dumps({
            'request_id': request_id.get(),
            'url_video': 'Как я вижу мужчин 2003 года рождения и как есть на самом деле.mp4'
        }).encode('utf-8')

        RequestDispatcher.create_waiter(request_id.get())

        logger.debug('Sending request to service_1')

        await cls.basic_send(cls.__worker_tasks_queue, data, correlation_id=request_id.get())

        logger.debug('Awaiting response from service_1')

        a = await RequestDispatcher.wait_for_result(request_id.get())
        return a
