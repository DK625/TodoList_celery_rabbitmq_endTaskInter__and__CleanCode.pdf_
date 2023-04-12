import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv

ROOT_PATH = os.path.dirname(__file__)
env_path = f"{ROOT_PATH}\.env"
load_dotenv(dotenv_path=env_path)


class Settings:
    DATABASE_URL: str = os.getenv("SQLALCHAMY_DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")


settings = Settings()
