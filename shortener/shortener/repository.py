import contextlib
import logging
import time

import aioboto3
from botocore.exceptions import ClientError

from . import settings
from .models import Redirect
from prometheus_client import Histogram


logger = logging.getLogger(__name__)

_dynamodb = {}


CREATE_REDIRECT_DURATION = Histogram(
    "shortener_create_redirect_duration_seconds",
    "Shortener create redirect duration (seconds)",
)
GET_REDIRECT_DURATION = Histogram(
    "shortener_get_redirect_duration_seconds",
    "Shortener get redirect duration (seconds)",
)


class RedirectRepositoryException(Exception):
    pass


class RedirectExistsException(RedirectRepositoryException):
    pass


class RedirectNotFoundException(RedirectRepositoryException):
    pass


class RedirectRepositoryUnavailableException(RedirectRepositoryException):
    pass


async def init_repository():
    context_stack = contextlib.AsyncExitStack()
    _dynamodb["context_stack"] = context_stack
    _dynamodb["resource"] = await context_stack.enter_async_context(
        aioboto3.resource("dynamodb", **settings.DYNAMODB)
    )
    if settings.CREATE_REDIRECTS_TABLE:
        await _dynamodb["resource"].create_table(**settings.REDIRECTS_TABLE_CONFIG)

    _dynamodb["redirects_table"] = await _dynamodb["resource"].Table(
        settings.REDIRECTS_TABLE
    )


async def close_repository():
    await _dynamodb["context_stack"].aclose()


async def create_redirect(redirect: Redirect) -> Redirect:
    if not redirect.url_id:
        redirect.url_id = Redirect.generate_url_id()

    try:
        with CREATE_REDIRECT_DURATION.time():
            await _dynamodb["redirects_table"].put_item(
                Item=redirect.dict(),
                ConditionExpression="attribute_not_exists(url_id)",
            )
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise RedirectExistsException()
        else:
            print(exc.response)
            logger.exception("create_redirect.client_error")
            raise RedirectRepositoryUnavailableException()
    except Exception:
        logger.exception("create_redirect.exception")
        raise RedirectRepositoryException()
    else:
        return redirect


async def get_redirect(url_id: str) -> Redirect:
    try:
        with GET_REDIRECT_DURATION.time():
            result = await _dynamodb["redirects_table"].get_item(Key={"url_id": url_id})
    except ClientError:
        logger.exception("get_redirect.client_error")
        raise RedirectRepositoryUnavailableException()
    except Exception:
        logger.exception("get_redirect.exception")
        raise RedirectRepositoryException()
    else:
        if "Item" in result:
            return Redirect(**result["Item"])
        else:
            raise RedirectNotFoundException()
