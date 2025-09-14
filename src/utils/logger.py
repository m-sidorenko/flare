import logging
import os
import sys
import logfire
from typing import Literal, TYPE_CHECKING
import pathlib

from loguru import logger
if TYPE_CHECKING:
    from loguru import Logger  # why so, check here https://loguru.readthedocs.io/en/stable/resources/troubleshooting.html

def setup_logger(
        root_path: pathlib.Path,
        service_name: str,
        log_level: str = "INFO",
        logfire_token: str | None = None,
        logfire_env: Literal['dev', 'prod'] | None = None,
):
    """
    Configures the logger for the application.
    :param root_path: The root path of the project. Used to create the logs directory.
    :param service_name: The name of the service for which the logger is being configured.
    :param log_level: The logging level to set for the logger.
    :param logfire_token: Optional Logfire token for remote logging.
    :param logfire_env: Optional environment name for Logfire. Could be 'dev' or 'prod'
    :return: None
    """
    logger.remove()

    # create logs directory if not exists
    log_absolute_path = os.path.join(
        root_path,
        "logs",
        f"{service_name}.log"
    )
    os.makedirs(
        os.path.dirname(log_absolute_path),
        exist_ok=True
    )

    # file handler
    logger.add(
        str(log_absolute_path),
        level=log_level,
        rotation="5 MB",
        compression="gz",

        retention="4 days",

        enqueue=True,
        backtrace=True,
        diagnose=True,
        catch=True
    )

    # stdout handler
    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
               "- <level>{message}</level>",
        colorize=True,
        backtrace=True,
        diagnose=True,
        catch=True
    )

    # add logfire handler if token is provided
    if logfire_token:
        logfire.configure(
            token=logfire_token,
            service_name=service_name,
            environment=logfire_env if logfire_env else 'dev',
            console=False
        )
        logger.add(
            **logfire.loguru_handler()
        )

    logger.info(
        f"Logger configured for service '{service_name}' with level '{log_level}'",
    )


def get_logger() -> "Logger":
    """
    Returns the configured logger instance.
    :return: logger instance
    """
    return logger
