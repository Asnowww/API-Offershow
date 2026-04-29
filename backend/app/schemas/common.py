from typing import Any

from pydantic import BaseModel, ConfigDict


class AnyPayload(BaseModel):
    model_config = ConfigDict(extra="allow")


def payload_dict(payload: Any) -> dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    if hasattr(payload, "model_dump"):
        return payload.model_dump(exclude_unset=True)
    return dict(payload)

