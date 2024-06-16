from app.models.products import ProductStatus
from app.repositories.common import BaseMixin, BulkActionsMixin, SearchMixin


class ProductStatusRepository(BaseMixin, BulkActionsMixin, SearchMixin):
    model = ProductStatus
