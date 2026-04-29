from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.response import ApiError, api_error_handler, error_response, validation_error_handler
from app.core.risk import risk_limiter
from app.routers import auth, common, companies, content, job_postings, salary_comments, salary_reports, search, users


settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def risk_control(request: Request, call_next):
    try:
        if request.url.path.startswith("/api/"):
            risk_limiter.check(request)
        return await call_next(request)
    except ApiError as exc:
        return error_response(exc.code, exc.message, exc.http_status)


app.add_exception_handler(ApiError, api_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)

api_prefix = "/api/v1"
app.include_router(common.router, prefix=api_prefix)
app.include_router(auth.router, prefix=api_prefix)
app.include_router(users.router, prefix=api_prefix)
app.include_router(companies.router, prefix=api_prefix)
app.include_router(job_postings.router, prefix=api_prefix)
app.include_router(salary_reports.router, prefix=api_prefix)
app.include_router(salary_comments.router, prefix=api_prefix)
app.include_router(content.router, prefix=api_prefix)
app.include_router(search.router, prefix=api_prefix)

