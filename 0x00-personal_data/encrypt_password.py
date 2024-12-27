#!/usr/bin/env python3

"""
Encrypting passwords
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password
    """

    salt = bcrypt.gensalt()
    password = password.encode("utf-8")
    return bcrypt.hashpw(password, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks it the password is valid
    """
    password = password.encode("utf-8")
    return bcrypt.checkpw(password, hashed_password)
