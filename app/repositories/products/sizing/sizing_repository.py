from app.models.products import Sizing
from app.repositories.common import BaseMixin, BulkActionsMixin, SearchMixin


class SizingRepository(BaseMixin, BulkActionsMixin, SearchMixin):
    model = Sizing
