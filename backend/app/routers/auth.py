from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import ApiError, ok
from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.models.entities import User
from app.schemas.common import AnyPayload, payload_dict
from app.services.serializers import user_out


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(payload: AnyPayload, db: Session = Depends(get_db)):
    data = payload_dict(payload)
    username = data.get("username", "")
    password = data.get("password", "")
    user = db.query(User).filter(User.username == username, User.deleted.is_(False)).first()
    if not user or not verify_password(password, user.password_hash):
        raise ApiError(40101, "账号或密码错误", 401)
    token = create_access_token(str(user.id), {"role": user.role})
    return ok({"token": token, "token_type": "bearer", "expires_in": 7200, "user": user_out(user)})


@router.post("/wx-login")
def wx_login(payload: AnyPayload, db: Session = Depends(get_db)):
    data = payload_dict(payload)
    if not data.get("code"):
        raise ApiError(40001, "缺少微信授权 code", 400)
    user = db.query(User).filter(User.username == "demo").first()
    token = create_access_token(str(user.id), {"role": user.role, "wx_mock": True})
    return ok({"token": token, "token_type": "bearer", "expires_in": 7200, "user": user_out(user)})


