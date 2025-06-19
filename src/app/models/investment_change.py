import __core.model as model

from app.models.investment import InvestmentModel

@model.dataclass
class InvestmentChangeModel(model.Model):
  id: str = model.field(default_factory=model.Model.GenUUID)
  created_at: str = model.field(default_factory=model.Model.GetTime)
  change: float = None

  investment_id: str = None
  fk_investment: InvestmentModel = None
