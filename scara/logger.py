import logging

logger = logging.getLogger("scara")
logging_handler = logging.StreamHandler()
logging_handler.setFormatter(
    logging.Formatter(
        "[log] %(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s"
    )
)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging_handler)
