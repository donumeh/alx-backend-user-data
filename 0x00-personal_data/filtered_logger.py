#!/usr/bin/env python3
"""Filter Datum"""
from datetime import datetime
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
    stream_handler.setFormatter(formatter)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    get_db: Returns a database connection
    """
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")
    user = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")

    db = mysql.connector.connect(
        database=db_name, user=user, password=password, host=host
    )
    return db


PII_FIELDS = ("email", "phone", "ssn", "password", "name")


def main() -> None:
    """
    Retrieve the database table and values
    """
    # get the database and execute sql script
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")

    for row in cursor:

        cols = [
            "name",
            "email",
            "phone",
            "ssn",
            "password",
            "ip",
            "last_login",
            "user_agent",
        ]
        record = list(row)

        updated_record = []
        col_cnt = 0
        for data in row:

            if col_cnt == "last_login":
                d = datetime.isoformat(data)
            else:
                d = data

            updated_record.append("{}={}".format(cols[col_cnt], d))
            col_cnt += 1
        updated_record = "; ".join(updated_record)
        redacting_formatter = RedactingFormatter(PII_FIELDS)

        log_record = logging.LogRecord(
            "user_data", logging.INFO, None, None, updated_record, None, None
        )
        obfuscated_msg = redacting_formatter.format(log_record)
        print(obfuscated_msg)
        logger = get_logger()

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
