import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt='%(asctime)s | %(levelname)-6s | %(funcName)s()#L%(lineno)-4d | %(message)s'))
logger.addHandler(handler)