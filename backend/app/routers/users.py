from typing import Optional

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.core.response import ok
from app.models.entities import User
from app.services.serializers import user_out


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def me(user: Optional[User] = Depends(get_current_user)):
    return ok(user_out(user) if user else None)

