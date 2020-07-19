from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette_exporter import PrometheusMiddleware

from . import logs, service_api


logs.setup()

app = FastAPI(title="Shortener", description="URL shortener API")

app.add_middleware(PrometheusMiddleware, app_name="shortener", group_paths=True)
app.add_middleware(SentryAsgiMiddleware)

app.include_router(service_api.router, tags=["service"])
