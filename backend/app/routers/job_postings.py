from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.deps import ensure_owner_or_admin, ensure_read_allowed, get_current_user, require_role
from app.core.response import ApiError, ok
from app.db.session import get_db
from app.models.entities import Company, JobPosting, User
from app.schemas.common import AnyPayload, payload_dict
from app.services.pagination import page_result, parse_page
from app.services.serializers import job_out


router = APIRouter(prefix="/job-postings", tags=["job-postings"])


JOB_FIELDS = [
    "company_id", "title", "batch", "recruitment_type", "industry", "cities", "deliver_start", "deliver_end",
    "graduation_range", "apply_url", "internal_code", "benefits", "positions", "tags", "intro_html", "views",
    "interest_count", "is_official",
]


def apply_job_data(job: JobPosting, data: dict) -> JobPosting:
    for key in JOB_FIELDS:
        if key in data:
            setattr(job, key, data[key])
    if "industry_code" in data:
        job.industry = data["industry_code"]
    if "description" in data and "intro_html" not in data:
        job.intro_html = data["description"]
    return job


def filter_jobs(query, q: str, industry: str, cities: str, recruitment_type: str, batch: str, has_internal_code: bool):
    if q:
        pattern = f"%{q}%"
        query = query.join(Company).filter(or_(JobPosting.title.ilike(pattern), Company.name.ilike(pattern)))
    if industry and industry != "all":
        query = query.filter(JobPosting.industry == industry)
    if recruitment_type:
        query = query.filter(JobPosting.recruitment_type == recruitment_type)
    if batch and batch != "不限":
        query = query.filter(JobPosting.batch == batch)
    if has_internal_code:
        query = query.filter(JobPosting.internal_code != "")
    rows = query.all() if cities else None
    if cities:
        wanted = [item for item in cities.split(",") if item]
        rows = [row for row in rows if any(city in (row.cities or []) for city in wanted)]
        return rows
    return query


@router.get("")
def list_jobs(
    q: str = "",
    industry: str = "",
    cities: str = "",
    recruitment_type: str = "",
    batch: str = "",
    has_internal_code: bool = False,
    sort: str = "latest",
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    ensure_read_allowed(user)
    page, page_size = parse_page(page, page_size)
    base = db.query(JobPosting).filter(JobPosting.deleted.is_(False))
    filtered = filter_jobs(base, q, industry, cities, recruitment_type, batch, has_internal_code)
    if isinstance(filtered, list):
        rows = sorted(filtered, key=lambda item: (item.views if sort == "hot" else item.created_at), reverse=sort != "deadline")
        total = len(rows)
        rows = rows[(page - 1) * page_size: page * page_size]
    else:
        if sort == "hot":
            filtered = filtered.order_by(JobPosting.views.desc())
        elif sort == "deadline":
            filtered = filtered.order_by(JobPosting.deliver_end.asc())
        else:
            filtered = filtered.order_by(JobPosting.created_at.desc(), JobPosting.id.desc())
        total = filtered.count()
        rows = filtered.offset((page - 1) * page_size).limit(page_size).all()
    return ok(page_result([job_out(row) for row in rows], total, page, page_size))


@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    job = db.get(JobPosting, job_id)
    if not job or job.deleted:
        raise ApiError(40401, "招聘信息不存在", 404)
    job.views += 1
    db.commit()
    db.refresh(job)
    return ok(job_out(job))


@router.post("")
def create_job(payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_role("hr"))):
    data = payload_dict(payload)
    company_id = data.get("company_id") or user.company_id
    if not company_id:
        raise ApiError(40001, "缺少 company_id", 400)
    if user.role == "hr" and user.company_id != int(company_id):
        raise ApiError(40301, "HR 只能创建本公司招聘信息", 403)
    company = db.get(Company, int(company_id))
    if not company:
        raise ApiError(40001, "公司不存在", 400)
    job = apply_job_data(JobPosting(company_id=company.id, industry=company.industry, title="", recruitment_type="campus", owner_user_id=user.id), data)
    db.add(job)
    db.commit()
    db.refresh(job)
    return ok(job_out(job))


@router.patch("/{job_id}")
def update_job(job_id: int, payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_role("hr"))):
    job = db.get(JobPosting, job_id)
    if not job or job.deleted:
        raise ApiError(40401, "招聘信息不存在", 404)
    ensure_owner_or_admin(user, job.owner_user_id, job.company_id)
    apply_job_data(job, payload_dict(payload))
    db.commit()
    db.refresh(job)
    return ok(job_out(job))


@router.put("/{job_id}")
def replace_job(job_id: int, payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_role("hr"))):
    data = payload_dict(payload)
    if "title" not in data or "company_id" not in data:
        raise ApiError(40001, "replace 需要完整招聘字段 title/company_id", 400)
    return update_job(job_id, payload, db, user)


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), user: User = Depends(require_role("hr"))):
    job = db.get(JobPosting, job_id)
    if not job or job.deleted:
        raise ApiError(40401, "招聘信息不存在", 404)
    ensure_owner_or_admin(user, job.owner_user_id, job.company_id)
    job.deleted = True
    db.commit()
    return ok({"id": job_id})


@router.post(":batchCreate")
def batch_create_jobs(payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_role("hr"))):
    success = 0
    ids = []
    errors = []
    for index, item in enumerate(payload_dict(payload).get("items", [])):
        try:
            company_id = int(item.get("company_id") or user.company_id)
            if user.role == "hr" and user.company_id != company_id:
                raise ValueError("HR 只能导入本公司招聘信息")
            company = db.get(Company, company_id)
            if not company:
                raise ValueError("公司不存在")
            job = apply_job_data(JobPosting(company_id=company_id, industry=company.industry, title="", recruitment_type="campus", owner_user_id=user.id), item)
            db.add(job)
            db.flush()
            ids.append(job.id)
            success += 1
        except Exception as exc:
            errors.append({"index": index, "msg": str(exc)})
    db.commit()
    return ok({"success": success, "failed": len(errors), "errors": errors, "ids": ids})


@router.post(":batchUpdate")
def batch_update_jobs(payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    success = 0
    errors = []
    for index, item in enumerate(payload_dict(payload).get("items", [])):
        try:
            job = db.get(JobPosting, int(item["id"]))
            if not job:
                raise ValueError("招聘信息不存在")
            apply_job_data(job, item)
            success += 1
        except Exception as exc:
            errors.append({"index": index, "msg": str(exc)})
    db.commit()
    return ok({"success": success, "failed": len(errors), "errors": errors})


@router.post(":batchDelete")
def batch_delete_jobs(payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    ids = payload_dict(payload).get("ids", [])
    rows = db.query(JobPosting).filter(JobPosting.id.in_(ids)).all()
    for row in rows:
        row.deleted = True
    db.commit()
    return ok({"success": len(rows), "failed": max(len(ids) - len(rows), 0), "errors": []})


@router.get("/{job_id}/positions")
def list_positions(job_id: int, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    job = db.get(JobPosting, job_id)
    if not job or job.deleted:
        raise ApiError(40401, "招聘信息不存在", 404)
    return ok({"items": job.positions or [], "total": len(job.positions or [])})


@router.post("/{job_id}/positions")
def create_position(job_id: int, payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_role("hr"))):
    job = db.get(JobPosting, job_id)
    if not job or job.deleted:
        raise ApiError(40401, "招聘信息不存在", 404)
    ensure_owner_or_admin(user, job.owner_user_id, job.company_id)
    positions = list(job.positions or [])
    data = payload_dict(payload)
    data["id"] = data.get("id") or (max([item.get("id", 0) for item in positions] or [0]) + 1)
    positions.append(data)
    job.positions = positions
    db.commit()
    return ok(data)
