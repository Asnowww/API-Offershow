from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.deps import ensure_read_allowed, get_current_user
from app.core.response import ok
from app.db.session import get_db
from app.models.entities import Company, JobPosting, SalaryReport, User
from app.services.pagination import page_result, parse_page
from app.services.serializers import company_out, job_out, salary_out


router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
def search(scope: str = "job", q: str = "", page: int = 1, page_size: int = 20, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    page, page_size = parse_page(page, page_size)
    pattern = f"%{q}%"
    if scope == "salary":
        query = db.query(SalaryReport).join(Company).filter(SalaryReport.deleted.is_(False))
        if q:
            query = query.filter(or_(Company.name.ilike(pattern), SalaryReport.position.ilike(pattern), SalaryReport.city.ilike(pattern)))
        total = query.count()
        rows = query.order_by(SalaryReport.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return ok(page_result([salary_out(row) for row in rows], total, page, page_size))
    if scope == "company":
        query = db.query(Company).filter(Company.deleted.is_(False))
        if q:
            query = query.filter(Company.name.ilike(pattern))
        total = query.count()
        rows = query.order_by(Company.id).offset((page - 1) * page_size).limit(page_size).all()
        return ok(page_result([company_out(row) for row in rows], total, page, page_size))
    query = db.query(JobPosting).join(Company).filter(JobPosting.deleted.is_(False))
    if q:
        query = query.filter(or_(Company.name.ilike(pattern), JobPosting.title.ilike(pattern)))
    total = query.count()
    rows = query.order_by(JobPosting.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return ok(page_result([job_out(row) for row in rows], total, page, page_size))

