import logging

def setup_custom_logger(name: str) -> logging.Logger:
    formatter = logging.Formatter(fmt='%(threadName)s:%(asctime)s- %(levelname)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger
