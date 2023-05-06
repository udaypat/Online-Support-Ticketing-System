import os
from datetime import timedelta

base_dir = os.path.abspath(os.path.dirname(__file__))

class LocalConfig():
    DEBUG = True
    LOCAL_URL = "http://localhost:5000"

    SQLITE_DB_DIR = os.path.join(base_dir, "../../db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "db.sqlite3")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_REGISTERABLE = True
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    SECURITY_USERNAME_ENABLE = True
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
    WTF_CSRF_CHECK_DEFAULT = False
    SESSION_COOKIE_SAMESITE = None
    USER_IMAGE_FOLDER = "static/images/profile"

    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "admin@smartSupport.com"
    SENDER_PASSWORD = ""

    JWT_SECRET_KEY = "SKBw2u4x246vBnTxBcGrwpUNjbvXZm"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=15)
