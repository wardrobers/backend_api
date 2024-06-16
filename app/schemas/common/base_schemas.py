from dataclasses import dataclass, field
from typing import Generic, TypeVar

DataT = TypeVar("DataT")


@dataclass
class PaginatedResponse(Generic[DataT]):
    """
    A detailed and tailored dataclass for paginated responses,
    designed to align with the ProductsRepository requirements.
    """

    items: list[DataT] = field(
        default_factory=list,
        metadata={"description": "The list of items for the requested page."},
    )
    page: int = field(
        default=1,
        metadata={"description": "The current page number (1-based indexing)."},
    )
    page_size: int = field(
        default=10, metadata={"description": "The number of items per page."}
    )
    total_count: int = field(
        default=0,
        metadata={"description": "The total number of items matching the query."},
    )
    total_pages: int = field(
        init=False,
        metadata={
            "description": "The total number of pages calculated from total_count and page_size."
        },
    )
    has_previous: bool = field(
        init=False,
        metadata={"description": "True if there is a previous page, False otherwise."},
    )
    has_next: bool = field(
        init=False,
        metadata={"description": "True if there is a next page, False otherwise."},
    )

    def __post_init__(self):
        self.total_pages = (self.total_count + self.page_size - 1) // self.page_size
        self.has_previous = self.page > 1
        self.has_next = self.page < self.total_pages
