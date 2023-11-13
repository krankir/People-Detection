from typing import Callable, Any
import asyncio


class AsyncTimedIterable:
    """
    Class, used for implement timeouts with 'async for' loops
    """

    def __init__(self, iterable: Any, timeout: float = None,
                 parser_callback: Callable = None) -> None:
        """
        Create an async timed iterable
        Args:
            iterable(Any): Iterable to wrap
            timeout(float): Timeout, None means no timeout
            parser_callback(Callable): Callback, applied to each received message, must return a tuple (Any, bool)
                Any means any result of message process, raw bytes, or other
                Bool means 'continue processing' or not
        Returns:
            None
        """

        class AsyncTimedIterator:
            """
            Inner class, that straightly implements a timeout between iterations
            """
            stop = False
            __parser_callback = parser_callback

            def __init__(self):
                self.__parser_callback = parser_callback
                self._iterator = iterable.__aiter__()

            async def __anext__(self):
                """
                Walks through the sequence. If callback returns False for the second parameter - StopAsyncIteration
                Raises:
                    StopAsyncIteration
                    TimeoutError
                """
                if self.stop:
                    raise StopAsyncIteration
                message = await asyncio.wait_for(self._iterator.__anext__(), timeout)
                async with message.process(ignore_processed=True, requeue=True):
                    if self.__parser_callback is not None:
                        result, self.stop = self.__parser_callback(message)
                        return result
                    return message.body

        self._factory = AsyncTimedIterator

    def __aiter__(self):
        """
        Returns an asynchronous iterator
        """
        return self._factory()
