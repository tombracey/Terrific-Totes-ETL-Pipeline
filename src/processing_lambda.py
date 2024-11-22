import logging


logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)


def processing_lambda_handler(event, context):
    output = event

    #insert code here 

    logger.info(output)
    return output