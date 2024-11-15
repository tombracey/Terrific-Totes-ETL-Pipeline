import logging


def lambda_handler(event, context):
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)
    logger.info("Logging a message!")
    logger.error("ERROR")
    return "Hello world"
