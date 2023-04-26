import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv

ROOT_PATH = os.path.dirname(__file__)
env_path = os.path.join(ROOT_PATH, '.env')

# env_path = f"{ROOT_PATH}\.env"
load_dotenv(dotenv_path=env_path)


class Settings:
    DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    BROKER_MESSAGE: str = os.getenv("BROKER_MESSAGE")
    EMAIL: str = os.getenv("EMAIL")
    PASSWORD: str = os.getenv("PASSWORD")


settings = Settings()
