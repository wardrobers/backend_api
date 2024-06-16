from app.models.products import Categories
from app.repositories.common import BaseMixin, BulkActionsMixin, SearchMixin


class CategoriesRepository(BaseMixin, BulkActionsMixin, SearchMixin):
    model = Categories
