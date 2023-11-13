import asyncio
import time
from typing import Any

from src.logger import logger


class RequestDispatcher(object):
    __futures = dict()

    @classmethod
    def create_waiter(cls, request_id: str):
        loop = asyncio.get_event_loop()
        fut = loop.create_future()
        cls.__futures[request_id] = (fut, time.time())

    @classmethod
    async def wait_for_result(cls, request_id: str, timeout: float = None):
        if request_id not in cls.__futures:
            raise KeyError(400, 'dhs-api', 'Future is not exists', 'Future, associated with request not exists')

        fut = cls.__futures[request_id][0]
        try:
            result = await asyncio.wait_for(fut, timeout)
            logger.debug(f"RequestDispatcher return result for {request_id}")
            return result
        except asyncio.TimeoutError as e:
            logger.debug(f"RequestDispatcher timeout for {request_id}")
            raise e
        finally:
            del cls.__futures[request_id]

    @classmethod
    def set_result(cls, request_id: str, result: Any) -> None:
        if request_id in cls.__futures and not cls.__futures[request_id][0].cancelled():
            logger.debug(f"RequestDispatcher set_result for {request_id}")
            cls.__futures[request_id][0].set_result(result)
