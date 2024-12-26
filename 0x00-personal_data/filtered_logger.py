#!/usr/bin/env python3
"""Filter Datum"""
import logging
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
