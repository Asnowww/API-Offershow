from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.deps import ensure_owner_or_admin, ensure_read_allowed, get_current_user, require_login, require_role
from app.core.response import ApiError, ok
from app.db.session import get_db
from app.models.entities import Company, SalaryComment, SalaryReport, User
from app.schemas.common import AnyPayload, payload_dict
from app.services.pagination import page_result, parse_page
from app.services.serializers import comment_out, salary_out


router = APIRouter(prefix="/salary-reports", tags=["salary-reports"])

SALARY_FIELDS = [
    "company_id", "position", "city", "salary_desc", "annual_min", "annual_max", "recruitment_type",
    "education", "edu_tags", "industry", "tags", "remark", "credibility", "views", "likes",
]


def apply_salary_data(report: SalaryReport, data: dict) -> SalaryReport:
    for key in SALARY_FIELDS:
        if key in data:
            setattr(report, key, data[key])
    if "industry_code" in data:
        report.industry = data["industry_code"]
    return report


def filtered_salary_query(db: Session, params: dict):
    query = db.query(SalaryReport).filter(SalaryReport.deleted.is_(False))
    q = params.get("q") or ""
    if q:
        query = query.join(Company)
        for token in [item for item in q.split() if item]:
            pattern = f"%{token}%"
            query = query.filter(or_(Company.name.ilike(pattern), SalaryReport.position.ilike(pattern), SalaryReport.city.ilike(pattern)))
    for key in ["recruitment_type", "education", "city"]:
        if params.get(key):
            query = query.filter(getattr(SalaryReport, key) == params[key])
    if params.get("industry") and params["industry"] != "all":
        query = query.filter(SalaryReport.industry == params["industry"])
    if params.get("salary_min") is not None:
        query = query.filter(SalaryReport.annual_max >= float(params["salary_min"]))
    if params.get("salary_max") is not None:
        query = query.filter(SalaryReport.annual_min <= float(params["salary_max"]))
    return query


@router.get("")
def list_salary_reports(
    q: str = "",
    recruitment_type: str = "",
    industry: str = "",
    education: str = "",
    city: str = "",
    salary_min: Optional[float] = None,
    salary_max: Optional[float] = None,
    sort: str = "latest",
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    ensure_read_allowed(user)
    page, page_size = parse_page(page, page_size)
    query = filtered_salary_query(db, locals())
    if sort == "hot":
        query = query.order_by((SalaryReport.views + SalaryReport.likes * 5).desc())
    elif sort == "credibility":
        query = query.order_by(SalaryReport.credibility.desc())
    else:
        query = query.order_by(SalaryReport.created_at.desc(), SalaryReport.id.desc())
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return ok(page_result([salary_out(row) for row in rows], total, page, page_size))


@router.get(":rank")
def salary_rank(period: str = "week", page: int = 1, page_size: int = 20, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    page, page_size = parse_page(page, page_size)
    query = db.query(SalaryReport).filter(SalaryReport.deleted.is_(False)).order_by((SalaryReport.views + SalaryReport.likes * 5).desc())
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return ok(page_result([salary_out(row) for row in rows], total, page, page_size))


@router.get("/{report_id}")
def get_salary_report(report_id: int, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    report = db.get(SalaryReport, report_id)
    if not report or report.deleted:
        raise ApiError(40401, "薪资爆料不存在", 404)
    report.views += 1
    db.commit()
    db.refresh(report)
    data = salary_out(report)
    data["comments_count"] = db.query(SalaryComment).filter(SalaryComment.salary_report_id == report_id, SalaryComment.deleted.is_(False)).count()
    return ok(data)


@router.post("")
def create_salary_report(payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_login)):
    if user.is_blacklisted:
        raise ApiError(40302, "风控拦截：当前用户禁止上传信息", 403)
    data = payload_dict(payload)
    company = db.get(Company, int(data.get("company_id", 0)))
    if not company:
        raise ApiError(40001, "公司不存在", 400)
    report = apply_salary_data(SalaryReport(company_id=company.id, industry=company.industry, position="", city="", salary_desc="", recruitment_type="campus", author_user_id=user.id), data)
    db.add(report)
    db.commit()
    db.refresh(report)
    return ok(salary_out(report))


@router.patch("/{report_id}")
def update_salary_report(report_id: int, payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_login)):
    report = db.get(SalaryReport, report_id)
    if not report or report.deleted:
        raise ApiError(40401, "薪资爆料不存在", 404)
    ensure_owner_or_admin(user, report.author_user_id)
    apply_salary_data(report, payload_dict(payload))
    db.commit()
    db.refresh(report)
    return ok(salary_out(report))


@router.put("/{report_id}")
def replace_salary_report(report_id: int, payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    data = payload_dict(payload)
    if "company_id" not in data or "position" not in data:
        raise ApiError(40001, "replace 需要完整薪资字段 company_id/position", 400)
    return update_salary_report(report_id, payload, db, user)


@router.delete("/{report_id}")
def delete_salary_report(report_id: int, db: Session = Depends(get_db), user: User = Depends(require_login)):
    report = db.get(SalaryReport, report_id)
    if not report or report.deleted:
        raise ApiError(40401, "薪资爆料不存在", 404)
    ensure_owner_or_admin(user, report.author_user_id)
    report.deleted = True
    db.commit()
    return ok({"id": report_id})


@router.post(":batchCreate")
def batch_create_salary_reports(payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    success = 0
    errors = []
    for index, item in enumerate(payload_dict(payload).get("items", [])):
        try:
            company = db.get(Company, int(item.get("company_id", 0)))
            if not company:
                raise ValueError("公司不存在")
            db.add(apply_salary_data(SalaryReport(company_id=company.id, industry=company.industry, position="", city="", salary_desc="", recruitment_type="campus", author_user_id=user.id), item))
            success += 1
        except Exception as exc:
            errors.append({"index": index, "msg": str(exc)})
    db.commit()
    return ok({"success": success, "failed": len(errors), "errors": errors})


@router.post(":batchUpdate")
def batch_update_salary_reports(payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    success = 0
    errors = []
    for index, item in enumerate(payload_dict(payload).get("items", [])):
        try:
            report = db.get(SalaryReport, int(item["id"]))
            if not report:
                raise ValueError("薪资爆料不存在")
            apply_salary_data(report, item)
            success += 1
        except Exception as exc:
            errors.append({"index": index, "msg": str(exc)})
    db.commit()
    return ok({"success": success, "failed": len(errors), "errors": errors})


@router.post(":batchDelete")
def batch_delete_salary_reports(payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    ids = payload_dict(payload).get("ids", [])
    rows = db.query(SalaryReport).filter(SalaryReport.id.in_(ids)).all()
    for row in rows:
        row.deleted = True
    db.commit()
    return ok({"success": len(rows), "failed": max(len(ids) - len(rows), 0), "errors": []})


@router.get("/{report_id}/comments")
def list_comments(report_id: int, page: int = 1, page_size: int = 20, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    page, page_size = parse_page(page, page_size)
    query = db.query(SalaryComment).filter(SalaryComment.salary_report_id == report_id, SalaryComment.deleted.is_(False)).order_by(SalaryComment.created_at.desc())
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return ok(page_result([comment_out(row) for row in rows], total, page, page_size))


@router.post("/{report_id}/comments")
def create_comment(report_id: int, payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_login)):
    report = db.get(SalaryReport, report_id)
    if not report or report.deleted:
        raise ApiError(40401, "薪资爆料不存在", 404)
    comment = SalaryComment(salary_report_id=report_id, user_id=user.id, content=payload_dict(payload).get("content", ""))
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return ok(comment_out(comment))

