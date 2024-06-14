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
    application = FastAPI(version="1.0.0")
    
    
    # Настройка CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    application.include_router(router)

   
    application.mount('/static', StaticFiles(directory='static'), 'static')
       
    return application


app = get_application()

@app.middleware("http")
async def log_request(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.options("/{path:path}")
async def options_handler(path: str):
    return {
        "allowed_methods": ["OPTIONS", "POST"]
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"detail": str(exc)})
