from app.models.products import StockKeepingUnits
from app.repositories.common import BaseMixin, BulkActionsMixin, SearchMixin


class StockKeepingUnitsRepository(BaseMixin, BulkActionsMixin, SearchMixin):
    model = StockKeepingUnits
