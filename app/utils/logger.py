"""Logging configuration for the Urban Rooftop Organic Farming Assistant."""

import logging
import sys


def setup_logger(name: str = "urban_farming_rag", level: int = logging.INFO) -> logging.Logger:
    """Configure and return a structured logger with formatting."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(level)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logger()
