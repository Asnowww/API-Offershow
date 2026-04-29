from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import ensure_owner_or_admin, require_login, require_role
from app.core.response import ApiError, ok
from app.db.session import get_db
from app.models.entities import SalaryComment, User
from app.schemas.common import AnyPayload, payload_dict
from app.services.serializers import comment_out


router = APIRouter(prefix="/salary-comments", tags=["salary-comments"])


@router.get("/{comment_id}")
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(SalaryComment, comment_id)
    if not comment or comment.deleted:
        raise ApiError(40401, "评论不存在", 404)
    return ok(comment_out(comment))


@router.patch("/{comment_id}")
def update_comment(comment_id: int, payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_login)):
    comment = db.get(SalaryComment, comment_id)
    if not comment or comment.deleted:
        raise ApiError(40401, "评论不存在", 404)
    ensure_owner_or_admin(user, comment.user_id)
    comment.content = payload_dict(payload).get("content", comment.content)
    db.commit()
    db.refresh(comment)
    return ok(comment_out(comment))


@router.put("/{comment_id}")
def replace_comment(comment_id: int, payload: AnyPayload, db: Session = Depends(get_db), user: User = Depends(require_login)):
    if "content" not in payload_dict(payload):
        raise ApiError(40001, "replace 需要 content", 400)
    return update_comment(comment_id, payload, db, user)


@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), user: User = Depends(require_login)):
    comment = db.get(SalaryComment, comment_id)
    if not comment or comment.deleted:
        raise ApiError(40401, "评论不存在", 404)
    ensure_owner_or_admin(user, comment.user_id)
    comment.deleted = True
    db.commit()
    return ok({"id": comment_id})

