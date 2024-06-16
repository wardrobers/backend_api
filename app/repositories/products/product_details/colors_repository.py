from app.models.products import Colors
from app.repositories.common import BaseMixin, BulkActionsMixin, SearchMixin


class ColorsRepository(BaseMixin, BulkActionsMixin, SearchMixin):
    model = Colors
