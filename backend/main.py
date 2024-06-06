from http import HTTPStatus

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.routers import router



def get_application() -> FastAPI:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]

    application = FastAPI(version="1.0.0", middleware=middleware)


    application.include_router(router)

   
    application.mount('/static', StaticFiles(directory='static'), 'static')
    return application


app = get_application()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"detail": str(exc)})
