import logging
from logging import Logger
from pathlib import Path
from time import time


class PRIME_Logger:
    def __init__(self, log_file: Path, name: str) -> None:
        # Variables to store timing information
        self.time: float = 0

        # Logger attributes
        self.logger_name: str = name.lower()
        self.log_file: Path = log_file.resolve()
        self.logger: Logger = logging.getLogger(name=self.logger_name)

        # Logger config
        logging.basicConfig(
            filename=self.log_file,
            encoding="utf-8",
            level=logging.DEBUG,
            format="%(asctime)s:%(levelname)s:%(message)s",
        )

    def start_timing(self, message: str) -> None:
        self.time = time()
        formatted_message: str = f"{message}: {self.time}"
        logging.info(msg=formatted_message)

    def end_timing(self, message: str) -> None:
        formatted_message: str = f"{message}: {time() - self.time} seconds"
        logging.info(msg=formatted_message)
