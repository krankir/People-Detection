import asyncio
import json
import multiprocessing
import uuid
from typing import Any, Tuple
import concurrent.futures
import aio_pika

from worker.app.amqp.base import RabbitMqHandlerBase
from worker.app.context import request_id
from worker.app.logger import logger
from worker.detected_face import process_video


class ServiceListener(RabbitMqHandlerBase):
    __instance_listen_queue = 'service_1'

    @staticmethod
    def get_workers():
        try:
            return multiprocessing.cpu_count()
        except NotImplementedError:
            return 4

    @classmethod
    async def listen(cls):
        logger.info(f"Starting listen queue {cls.__instance_listen_queue}")
        # workers = cls.get_workers()

        # with concurrent.futures.ProcessPoolExecutor() as executor:
        #     for i in range(workers):
        def response_parser(message: aio_pika.Message) -> Tuple[Any, bool]:
            response = json.loads(message.body.decode('utf-8'))
            request_id.set(response['request_id'])

            return response, False

        async for response in cls.basic_receive(cls.__instance_listen_queue,
                                                parser_callback=response_parser,
                                                exclusive_queue=True):
            logger.debug('New request')
            logger.info(f'video url = {response["url_video"]}')
            # a = executor.submit(process_video, response['url_video'])
            response['result'] = process_video(response['url_video'])
            logger.debug('Processing success')
            await cls.basic_send(f"{cls.__instance_listen_queue}_results",
                                         json.dumps(response).encode('utf-8'),
                                         correlation_id=response['request_id'])
