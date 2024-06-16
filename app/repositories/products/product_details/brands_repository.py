from app.models.products import Brands
from app.repositories.common import BaseMixin, BulkActionsMixin, SearchMixin


class BrandsRepository(BaseMixin, BulkActionsMixin, SearchMixin):
    model = Brands
