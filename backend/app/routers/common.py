from fastapi import APIRouter

from app.core.response import ok
from app.scripts.seed_data import BATCHES, CITIES, INDUSTRIES, RECRUITMENT_TYPES


router = APIRouter(tags=["common"])


@router.get("/health")
def health():
    return ok({"status": "ok"})


@router.get("/dicts/industries")
def industries():
    return ok(INDUSTRIES)


@router.get("/dicts/cities")
def cities():
    return ok(CITIES)


@router.get("/dicts/batches")
def batches():
    return ok(BATCHES)


@router.get("/dicts/recruitment-types")
def recruitment_types():
    return ok(RECRUITMENT_TYPES)

