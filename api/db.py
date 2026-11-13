"""
BloodLink — Database connection module.

Loads credentials from .env and exposes a reusable connection function.
"""

import os
import pymysql
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()


def get_connection():
    """Return a new MySQL connection using credentials from .env."""
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "bloodlink_db"),
        port=int(os.getenv("DB_PORT", "3306")),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )