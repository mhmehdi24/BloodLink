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
        verify = os.getenv("DB_SSL_VERIFY", "true").lower() not in ("false", "0")
        connect_kwargs["ssl_verify_cert"] = verify
        connect_kwargs["ssl_verify_identity"] = verify

    try:
        return pymysql.connect(**connect_kwargs)
    except pymysql.err.OperationalError:
        # If strict SSL verification failed on a serverless container, retry with encryption enabled without strict cert check
        if is_cloud_db and connect_kwargs.get("ssl_verify_cert"):
            connect_kwargs["ssl_verify_cert"] = False
            connect_kwargs["ssl_verify_identity"] = False
            return pymysql.connect(**connect_kwargs)
        raise