"""Global journal utilities. Use the `logger` to log into journal."""
import logging

from exputils import utils

if utils.jrnl is None:
    
    logger = logging.getLogger(utils.jrnl_config["title"])
    handler = logging.FileHandler(utils.jrnl_config["name"])
    formatter = logging.Formatter(utils.jrnl_config["msg"], style="{")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    logger.info("START: Journal {}".format(utils.jrnl_config["name"]))

    utils.jrnl = logger.info
