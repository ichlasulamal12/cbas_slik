"""
==============================================================================
Project : CBAS SLIK Feature Engineering
File    : logger.py
Author  : Ichlasul Amal
Version : 1.0.0
==============================================================================

Logging Utility

"""

import logging
from pathlib import Path


# =============================================================================
# LOGGER
# =============================================================================

_LOGGER_INITIALIZED = False


# =============================================================================
# SETUP LOGGER
# =============================================================================

def setup_logger(
    log_dir="logs",
    log_file="cbas_slik.log",
    level=logging.INFO,
):

    global _LOGGER_INITIALIZED

    if _LOGGER_INITIALIZED:
        return

    Path(log_dir).mkdir(
        parents=True,
        exist_ok=True,
    )

    formatter = logging.Formatter(

        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",

        datefmt="%Y-%m-%d %H:%M:%S",

    )

    root_logger = logging.getLogger()

    root_logger.setLevel(level)

    # -------------------------------------------------------------------------
    # File Handler
    # -------------------------------------------------------------------------

    file_handler = logging.FileHandler(

        Path(log_dir) / log_file,

        encoding="utf-8",

    )

    file_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)

    # -------------------------------------------------------------------------
    # Console Handler
    # -------------------------------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)

    _LOGGER_INITIALIZED = True


# =============================================================================
# GET LOGGER
# =============================================================================

def get_logger(name):

    return logging.getLogger(name)


# =============================================================================
# CHANGE LEVEL
# =============================================================================

def set_log_level(level):

    logging.getLogger().setLevel(level)


# =============================================================================
# SHUTDOWN
# =============================================================================

def shutdown_logger():

    logging.shutdown()
