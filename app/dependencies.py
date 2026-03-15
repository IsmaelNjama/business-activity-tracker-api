import boto3
import json
import os
from functools import lru_cache


@lru_cache(maxsize=1)
def get_db_credentials():
    client = boto3.client(
        "secretsmanager", region_name=os.environ["APP_AWS_REGION"])
    secret = client.get_secret_value(SecretId=os.environ["SECRET_ARN"])
    data = json.loads(secret["SecretString"])
    return {"username": data["DB_USER"], "password": data["DB_PASSWORD"]}
