from math import ceil
from typing import Any, Iterable


def parse_page(page: int = 1, page_size: int = 20) -> tuple[int, int]:
    page = max(int(page or 1), 1)
    page_size = min(max(int(page_size or 20), 1), 50)
    return page, page_size


def page_result(items: Iterable[Any], total: int, page: int, page_size: int) -> dict:
    pages = ceil(total / page_size) if total else 0
    return {
        "items": list(items),
        "page": page,
        "page_size": page_size,
        "total": total,
        "pages": pages,
        "has_more": page < pages,
        "next_page_token": str(page + 1) if page < pages else None,
    }

