import os


DYNAMODB = {
    "endpoint_url": os.environ.get("DYNAMODB_ENDPOINT_URL", "None"),
    "region_name": os.environ.get("DYNAMODB_REGION_NAME", "None"),
    "aws_access_key_id": os.environ.get("DYNAMODB_AWS_ACCESS_KEY_ID", "None"),
    "aws_secret_access_key": os.environ.get("DYNAMODB_AWS_SECRET_ACCESS_KEY", "None"),
}


REDIRECTS_TABLE_CONFIG = {
    "BillingMode": "PAY_PER_REQUEST",
    "KeySchema": [{"AttributeName": "url_id", "KeyType": "HASH"}],
    "AttributeDefinitions": [{"AttributeName": "url_id", "AttributeType": "S"}],
}
REDIRECTS_TABLE = os.environ.get("REDIRECTS_TABLE", "redirects")
REDIRECTS_TABLE_CONFIG["TableName"] = REDIRECTS_TABLE
CREATE_REDIRECTS_TABLE = os.environ.get("CREATE_REDIRECTS_TABLE")


LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")

SENTRY_DSN = os.environ.get("SENTRY_DSN")
