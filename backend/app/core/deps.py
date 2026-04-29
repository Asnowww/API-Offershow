from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.response import ApiError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.entities import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)
ROLE_LEVEL = {"guest": 0, "user": 1, "member": 2, "hr": 3, "admin": 4}


def get_current_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme),
) -> Optional[User]:
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except Exception as exc:
        raise ApiError(40101, "未登录 / Token 失效", 401) from exc
    user = db.get(User, user_id)
    if not user or user.deleted:
        raise ApiError(40101, "未登录 / Token 失效", 401)
    return user


def require_login(user: Optional[User] = Depends(get_current_user)) -> User:
    if not user:
        raise ApiError(40101, "请先登录", 401)
    return user


def require_role(min_role: str):
    def checker(user: User = Depends(require_login)) -> User:
        if ROLE_LEVEL.get(user.role, 0) < ROLE_LEVEL[min_role]:
            raise ApiError(40301, "无权限", 403)
        if user.is_blacklisted:
            raise ApiError(40302, "风控拦截：当前用户禁止写入", 403)
        return user

    return checker


def ensure_read_allowed(user: Optional[User]) -> None:
    if user and user.is_crawler:
        raise ApiError(40302, "风控拦截：疑似爬虫用户禁止获取信息", 403)


def ensure_owner_or_admin(user: User, owner_id: Optional[int], company_id: Optional[int] = None) -> None:
    if user.role == "admin":
        return
    if owner_id and owner_id == user.id:
        return
    if user.role == "hr" and company_id and user.company_id == company_id:
        return
    raise ApiError(40301, "无权限", 403)

