import logging

from fastapi import APIRouter
from starlette_exporter import handle_metrics

logger = logging.getLogger(__name__)

router = APIRouter()
router.add_route("/metrics", handle_metrics)


@router.get("/ping")
async def ping():
    return {"ping": "pong"}


@router.get("/raise")
async def _raise():
    raise Exception("This a test exception")


@router.get("/log")
async def _log():
    logger.debug("This a test log")
    logger.info("This a test log")
    logger.warning("This a test log", stack_info=True)
    try:
        raise Exception("This a test exception")
    except Exception:
        logger.exception("This a test log")

    logger.critical("This a test log")
    return "OK"
