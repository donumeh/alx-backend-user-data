#!/usr/bin/env python3
"""Filter Datum"""
import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Filter datum returns the log message obfuscated"""
    return re.sub(r'(' + '|'.join(fields) + r')=[^' + re.escape(separator) + r';]+', r'\1=' + redaction, message)

