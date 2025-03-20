import __core.model as model

@model.dataclass
class InvestmentSourceModel(model.Model):
  id: str = model.field(default_factory=model.Model.GenUUID)
  created_at: str = model.field(default_factory=model.Model.GetTime)
  updated_at: str = model.field(default_factory=model.Model.GetTime)
  name: str = None
  code: str = None
  logo: str | None = None
