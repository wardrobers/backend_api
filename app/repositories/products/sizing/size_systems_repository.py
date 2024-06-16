from app.models.products import SizeSystems
from app.repositories.common import BaseMixin, BulkActionsMixin, SearchMixin


class SizeSystemsRepository(BaseMixin, BulkActionsMixin, SearchMixin):
    model = SizeSystems
