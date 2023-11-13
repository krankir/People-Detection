from app.amqp.listener import ServiceListener
import asyncio
from app.logger import logger

if __name__ == '__main__':
    logger.info("Starting worker")
    asyncio.run(ServiceListener.listen())

