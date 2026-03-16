import boto3
import json
import os
from functools import lru_cache
from dotenv import load_dotenv


@lru_cache(maxsize=1)
def get_secrets() -> dict:
    if os.environ.get("SECRET_ARN"):
        client = boto3.client("secretsmanager", region_name=os.environ["APP_AWS_REGION"])
        secret = client.get_secret_value(SecretId=os.environ["SECRET_ARN"])
        return json.loads(secret["SecretString"])

    load_dotenv()
    return {
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT", "5432"),
        "DB_NAME": os.getenv("DB_NAME", "postgres"),
        "SECRET_KEY": os.getenv("SECRET_KEY"),
    }


def get_db_credentials():
    secrets = get_secrets()
    return {"username": secrets["DB_USER"], "password": secrets["DB_PASSWORD"]}
