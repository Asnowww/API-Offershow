from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_role, ensure_read_allowed
from app.core.response import ApiError, ok
from app.db.session import get_db
from app.models.entities import Company, User
from app.schemas.common import AnyPayload, payload_dict
from app.services.pagination import page_result, parse_page
from app.services.serializers import company_out


router = APIRouter(prefix="/companies", tags=["companies"])


def apply_company_data(company: Company, data: dict) -> Company:
    for key in ["name", "logo_text", "logo_color", "industry", "intro"]:
        if key in data:
            setattr(company, key, data[key])
    return company


@router.get("")
def list_companies(
    q: str = "",
    industry: str = "",
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    ensure_read_allowed(user)
    page, page_size = parse_page(page, page_size)
    query = db.query(Company).filter(Company.deleted.is_(False))
    if q:
        pattern = f"%{q}%"
        query = query.filter(or_(Company.name.ilike(pattern), Company.intro.ilike(pattern)))
    if industry and industry != "all":
        query = query.filter(Company.industry == industry)
    total = query.count()
    rows = query.order_by(Company.id).offset((page - 1) * page_size).limit(page_size).all()
    return ok(page_result([company_out(item) for item in rows], total, page, page_size))


@router.get("/{company_id}")
def get_company(company_id: int, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ensure_read_allowed(user)
    company = db.get(Company, company_id)
    if not company or company.deleted:
        raise ApiError(40401, "公司不存在", 404)
    return ok(company_out(company))


@router.post("")
def create_company(payload: AnyPayload, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    company = apply_company_data(Company(industry="other"), payload_dict(payload))
    db.add(company)
    db.commit()
    db.refresh(company)
    return ok(company_out(company))


@router.patch("/{company_id}")
def update_company(company_id: int, payload: AnyPayload, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    company = db.get(Company, company_id)
    if not company or company.deleted:
        raise ApiError(40401, "公司不存在", 404)
    apply_company_data(company, payload_dict(payload))
    db.commit()
    db.refresh(company)
    return ok(company_out(company))


@router.put("/{company_id}")
def replace_company(company_id: int, payload: AnyPayload, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    data = payload_dict(payload)
    required = ["name", "industry"]
    if any(key not in data for key in required):
        raise ApiError(40001, "replace 需要完整公司字段 name/industry", 400)
    return update_company(company_id, payload, db, _)


@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    company = db.get(Company, company_id)
    if not company or company.deleted:
        raise ApiError(40401, "公司不存在", 404)
    company.deleted = True
    db.commit()
    return ok({"id": company_id})


@router.post(":batchCreate")
def batch_create_companies(payload: AnyPayload, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    items = payload_dict(payload).get("items", [])
    success = 0
    errors = []
    for index, item in enumerate(items):
        try:
            db.add(apply_company_data(Company(industry="other"), item))
            success += 1
        except Exception as exc:
            errors.append({"index": index, "msg": str(exc)})
    db.commit()
    return ok({"success": success, "failed": len(errors), "errors": errors})
