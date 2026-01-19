import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.application.exceptions.exceptions import (
    NoResultFoundException,
    DatabaseException,
)
from src.infrastructure.api.routes.product import router as product_router
from src.utils.logs import get_logger

logger = get_logger(__name__)


def additional_exception_handlers(app: FastAPI):
    @app.exception_handler(NoResultFoundException)
    async def no_result_found_exception_handler(
        request: Request, exc: NoResultFoundException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DatabaseException)
    async def database_exception_handler(request: Request, exc: DatabaseException):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )


def http_middleware(app: FastAPI):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        logger.info(f"Incoming request: {request.method} {request.url}")
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"Response status: {response.status_code} for {request.method} {request.url} - Process time: {process_time:.2f}ms"
        )
        return response


def create_app() -> FastAPI:
    app = FastAPI(
        title="Stoq API",
        description="API for Stoq e-commerce platform",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(product_router, prefix="/api/v1")

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    http_middleware(app)
    additional_exception_handlers(app)

    return app


app = create_app()
