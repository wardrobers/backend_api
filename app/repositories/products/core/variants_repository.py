from app.models.products import Variants
from app.repositories.common import BaseMixin, BulkActionsMixin, SearchMixin


class VariantsRepository(BaseMixin, BulkActionsMixin, SearchMixin):
    model = Variants
