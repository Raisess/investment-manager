import __core.model as model

from app.models.investment_rentability import InvestmentRentabilityModel
from app.models.investment_source import InvestmentSourceModel
from app.models.investment_type import InvestmentTypeModel

@model.dataclass
class InvestmentModel(model.Model):
  id: str = model.field(default_factory=model.Model.GenUUID)
  created_at: str = model.field(default_factory=model.Model.GetTime)
  updated_at: str = model.field(default_factory=model.Model.GetTime)
  user_id: str = None
  name: str = None
  invested: float = None
  total: float = None
  maturity: str = None

  fk_change: float = None

  type_id: str = None
  fk_type: InvestmentTypeModel = None

  source_id: str = None
  fk_source: InvestmentSourceModel = None

  rentability_id: str | None = None
  rentability_number: float | None = None
  fk_rentability: InvestmentRentabilityModel | None = None
