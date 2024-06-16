from app.models.products import Materials
from app.repositories.common import BaseMixin, BulkActionsMixin, SearchMixin


class MaterialsRepository(BaseMixin, BulkActionsMixin, SearchMixin):
    model = Materials
