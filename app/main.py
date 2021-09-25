from fastapi import FastAPI

from app.config import PROJECT_NAME, VERSION
from app.routes import pokemon


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, version=VERSION)

    application.include_router(pokemon.router, tags=["pokemon"], prefix="/pokemon")

    return application


app = get_application()
