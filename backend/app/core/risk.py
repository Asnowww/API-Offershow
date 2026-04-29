import time
from collections import defaultdict, deque
from typing import Deque

from fastapi import Request
from redis import Redis

from app.core.config import get_settings
from app.core.response import ApiError


class RiskLimiter:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.redis = None
        if self.settings.redis_url:
            self.redis = Redis.from_url(self.settings.redis_url, decode_responses=True)
        self.local_hits: dict[str, Deque[float]] = defaultdict(deque)

    def check(self, request: Request) -> None:
        key = request.headers.get("authorization") or request.client.host if request.client else "unknown"
        now = time.time()
        window = 60
        max_hits = 240
        if self.redis:
            redis_key = f"risk:{key}"
            count = self.redis.incr(redis_key)
            if count == 1:
                self.redis.expire(redis_key, window)
            if count > max_hits:
                raise ApiError(42901, "触发限流", 429)
            return
        bucket = self.local_hits[key]
        while bucket and now - bucket[0] > window:
            bucket.popleft()
        bucket.append(now)
        if len(bucket) > max_hits:
            raise ApiError(42901, "触发限流", 429)


risk_limiter = RiskLimiter()

