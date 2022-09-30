import logging
from logging.handlers import TimedRotatingFileHandler

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import config
from api.routers import router_v1
from main_kafka import producer


# DEFINE APP
app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/openapi.json", docs_url="/api/docs", redoc_url="/api/redoc")


# HANDLE LOG FILE
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = TimedRotatingFileHandler('{}{}-{}-{}_{}h-00p-00.log'.format(
    config.DL_LOG,
    config.u.year, config.u.month, config.u.day, config.u.hour),
    when="midnight", interval=1, encoding='utf8'
)
handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# ROUTER CONFIG
app.include_router(router_v1, prefix="/api/v1")


# CORS MIDDLEWARE
# origins = [
#    "http://{host}:{port}".format(host=config.HOST, port=config.PORT),
#    "http://{host}:{port}".format(host=config.HOST, port=config.FE_PORT),
#    "http://{host}".format(host=config.NGINX_HOST),
# ]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Start up event for FastAPI application."""
    logger.info("Starting up...")
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event for FastAPI application."""

    logger.info("Shutting down...")
    await producer.stop()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8081)
