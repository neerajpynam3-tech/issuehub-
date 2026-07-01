from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    """A page of results plus the totals the frontend needs to paginate."""

    items: list[T]
    total: int
    page: int
    page_size: int
