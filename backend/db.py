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
    host = os.getenv("DB_HOST", "localhost")
    default_port = 4000 if "tidb" in host.lower() else 3306
    port = int(os.getenv("DB_PORT", default_port))

    connect_kwargs = {
        "host": host,
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "bloodlink_db"),
        "port": port,
        "cursorclass": pymysql.cursors.DictCursor,
        "autocommit": False,
    }

    # Enable SSL if connecting to TiDB Cloud or if DB_SSL is true
    ssl_env = os.getenv("DB_SSL", "").lower()
    is_cloud_db = "tidbcloud.com" in host.lower() or "aivencloud.com" in host.lower() or ssl_env in ("true", "1")

    if is_cloud_db and ssl_env not in ("false", "0"):
        connect_kwargs["ssl_verify_cert"] = True
        connect_kwargs["ssl_verify_identity"] = True

    return pymysql.connect(**connect_kwargs)