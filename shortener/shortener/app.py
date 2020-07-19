from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette_exporter import PrometheusMiddleware

from . import api, logs, repository, service_api


logs.setup()

app = FastAPI(title="Shortener", description="URL shortener API")

app.add_middleware(PrometheusMiddleware, app_name="shortener", group_paths=True)
app.add_middleware(SentryAsgiMiddleware)

app.include_router(service_api.router, tags=["service"])
app.include_router(api.router, prefix="/redirects", tags=["redirects"])


@app.on_event("startup")
async def startup():
    await repository.init_repository()


@app.on_event("shutdown")
async def shutdown():
    await repository.close_repository()
