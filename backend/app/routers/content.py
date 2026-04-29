from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.deps import ensure_read_allowed, get_current_user, require_login, require_role
from app.core.response import ApiError, ok
from app.db.session import get_db
from app.models.entities import Company, ContentColumn, Course, EliteProgram, JobPosting, Review, SalaryReport, User
from app.schemas.common import AnyPayload, payload_dict
from app.services.pagination import page_result, parse_page
from app.services.serializers import column_out, course_out, elite_out, job_out, review_rank_out, salary_out


router = APIRouter(tags=["content"])


@router.get("/daily-briefs")
def daily_briefs(page: int = 1, page_size: int = 20, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    page, page_size = parse_page(page, page_size)
    query = db.query(JobPosting).filter(JobPosting.deleted.is_(False), JobPosting.id >= 1000, JobPosting.id <= 1029).order_by(JobPosting.id.asc())
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return ok(page_result([job_out(row) for row in rows], total, page, page_size))


@router.get("/courses")
def courses(q: str = "", category: str = "", page: int = 1, page_size: int = 20, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    page, page_size = parse_page(page, page_size)
    query = db.query(Course).filter(Course.deleted.is_(False))
    if q:
        query = query.filter(Course.title.ilike(f"%{q}%"))
    if category and category != "全部课程":
        query = query.filter(Course.category == category)
    total = query.count()
    rows = query.order_by(Course.id).offset((page - 1) * page_size).limit(page_size).all()
    return ok(page_result([course_out(row) for row in rows], total, page, page_size))


@router.get("/columns")
def columns(scope: str = "job", page: int = 1, page_size: int = 20, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    page, page_size = parse_page(page, page_size)
    query = db.query(ContentColumn).filter(ContentColumn.deleted.is_(False), ContentColumn.scope == scope)
    total = query.count()
    rows = query.order_by(ContentColumn.id).offset((page - 1) * page_size).limit(page_size).all()
    return ok(page_result([column_out(row) for row in rows], total, page, page_size))


@router.get("/columns/{column_id}")
def get_column(column_id: int, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    column = db.get(ContentColumn, column_id)
    if not column or column.deleted:
        raise ApiError(40401, "专栏不存在", 404)
    return ok(column_out(column))


def apply_column_job_filter(query, rule: dict):
    if rule.get("industry"):
        query = query.filter(JobPosting.industry == rule["industry"])
    if rule.get("recruitment_type"):
        query = query.filter(JobPosting.recruitment_type == rule["recruitment_type"])
    return query


def apply_salary_rule(query, rule: dict):
    if rule.get("industry"):
        query = query.filter(SalaryReport.industry == rule["industry"])
    if rule.get("annual_min_gte") is not None:
        query = query.filter(SalaryReport.annual_max >= float(rule["annual_min_gte"]))
    if rule.get("annual_min_lte") is not None:
        query = query.filter(SalaryReport.annual_max <= float(rule["annual_min_lte"]))
    if rule.get("company_id_any"):
        query = query.filter(SalaryReport.company_id.in_(rule["company_id_any"]))
    rows = query.all()
    if rule.get("position_any"):
        rows = [row for row in rows if row.position in rule["position_any"]]
    if rule.get("edu_tags_any"):
        rows = [row for row in rows if any(tag in (row.edu_tags or []) for tag in rule["edu_tags_any"])]
    return rows


@router.get("/columns/{column_id}/items")
def column_items(column_id: int, page: int = 1, page_size: int = 20, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    page, page_size = parse_page(page, page_size)
    column = db.query(ContentColumn).filter(ContentColumn.scope == "job", ContentColumn.source_id == column_id).first() or db.get(ContentColumn, column_id)
    if not column:
        raise ApiError(40401, "专栏不存在", 404)
    query = apply_column_job_filter(db.query(JobPosting).filter(JobPosting.deleted.is_(False)), column.filter_rule or {})
    total = query.count()
    rows = query.order_by(JobPosting.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return ok(page_result([job_out(row) for row in rows], total, page, page_size))


@router.get("/columns/{column_id}/salary-items")
def column_salary_items(column_id: int, page: int = 1, page_size: int = 20, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    page, page_size = parse_page(page, page_size)
    column = db.query(ContentColumn).filter(ContentColumn.scope == "salary", ContentColumn.source_id == column_id).first() or db.get(ContentColumn, column_id)
    if not column:
        raise ApiError(40401, "专栏不存在", 404)
    rows = apply_salary_rule(db.query(SalaryReport).filter(SalaryReport.deleted.is_(False)), column.filter_rule or {})
    rows = sorted(rows, key=lambda item: item.created_at, reverse=True)
    total = len(rows)
    rows = rows[(page - 1) * page_size: page * page_size]
    return ok(page_result([salary_out(row) for row in rows], total, page, page_size))


@router.get("/companies:reviewRank")
def review_rank(q: str = "", tab: str = "high", page: int = 1, page_size: int = 20, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    page, page_size = parse_page(page, page_size)
    query = db.query(Review).join(Company).filter(Review.deleted.is_(False))
    if q:
        query = query.filter(Company.name.ilike(f"%{q}%"))
    rows = query.all()
    if tab == "low":
        rows = sorted(rows, key=lambda item: item.score)
    elif tab == "hot":
        rows = sorted(rows, key=lambda item: item.review_count, reverse=True)
    elif tab == "high":
        rows = sorted(rows, key=lambda item: item.score, reverse=True)
    else:
        rows = sorted(rows, key=lambda item: item.id)
    total = len(rows)
    rows = rows[(page - 1) * page_size: page * page_size]
    return ok(page_result([review_rank_out(row, idx + 1 + (page - 1) * page_size) for idx, row in enumerate(rows)], total, page, page_size))


@router.post("/reviews")
def create_review(payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_login)):
    data = payload_dict(payload)
    company = db.get(Company, int(data.get("company_id", 0)))
    if not company:
        raise ApiError(40001, "公司不存在", 400)
    review = Review(company_id=company.id, user_id=user.id, score=float(data.get("score", 8.0)), content=data.get("content", ""))
    db.add(review)
    db.commit()
    db.refresh(review)
    return ok(review_rank_out(review, 1))


@router.get("/elite-programs")
def elite_programs(q: str = "", page: int = 1, page_size: int = 20, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    page, page_size = parse_page(page, page_size)
    query = db.query(EliteProgram).outerjoin(Company).filter(EliteProgram.deleted.is_(False))
    if q:
        pattern = f"%{q}%"
        query = query.filter(or_(EliteProgram.name.ilike(pattern), Company.name.ilike(pattern)))
    total = query.count()
    rows = query.order_by(EliteProgram.id).offset((page - 1) * page_size).limit(page_size).all()
    return ok(page_result([elite_out(row) for row in rows], total, page, page_size))


@router.post("/subscriptions")
def subscriptions(payload: AnyPayload, user: User = Depends(require_login)):
    return ok({"type": payload_dict(payload).get("type", "daily"), "status": "on", "user_id": user.id})


@router.post("/courses")
def create_course(payload: AnyPayload, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    data = payload_dict(payload)
    course = Course(title=data.get("title", ""), cover_color=data.get("cover_color", "#1E6EFF"), category=data.get("category", "求职必备"), price=int(data.get("price", 0)), intro=data.get("intro", ""))
    db.add(course)
    db.commit()
    db.refresh(course)
    return ok(course_out(course))
