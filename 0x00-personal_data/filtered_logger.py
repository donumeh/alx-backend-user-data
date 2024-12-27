#!/usr/bin/env python3
"""Filter Datum"""
import logging
import mysql.connector
import os
import re
from typing import List


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log message
        """
        obfuscated_str = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
        )

        return self._fmt % {
            "name": record.name,
            "message": obfuscated_str,
            "levelname": record.levelname,
            "asctime": self.formatTime(record, self.datefmt),
        }


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Filter datum returns the log message obfuscated"""
    return re.sub(
        r"(" + "|".join(fields) + r")=[^" + re.escape(separator) + r";]+",
        r"\1=" + redaction,
        message,
    )


def get_logger() -> logging.Logger:
    """
    Get logger takes no argument and returns logging.Logger
    """
    # create logger
    logger: logging.Logger = logging.getLogger("user_data")
    # set logger level
    logger.setLevel(logging.INFO)
    # set logger propagate
    logger.propagate = False
    # create log message formatter variable
    formatter = RedactingFormatter.FORMAT
    # handles stream handler
    stream_handler = logging.StreamHandler()
    # adds handler to logger
    logger.addHandler(stream_handler)
    # lastly set the formatter using `formatter` variable
    logger.setFormatter(formatter)


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    get_db: Returns a database connection
    """

    db = mysql.connector.connect(
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        port=3306,
    )
    return db


PII_FIELDS = ("email", "phone", "ssn", "password", "name")
