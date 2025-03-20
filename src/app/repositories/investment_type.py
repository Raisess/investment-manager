from __core.plugins.database.sql.postgresql import PostgreSQL
from __core.repository import Repository

from app.models import InvestmentTypeModel

class InvestmentTypeRepository(Repository):
  def __init__(self):
    self.__table = "investment_types"
    self.__database = PostgreSQL()

  def find(self) -> list[InvestmentTypeModel]:
    results = self.__database.select(self.__table, {})
    return [InvestmentTypeRepository.__format(item) for item in results]

  @staticmethod
  def __format(data: dict) -> InvestmentTypeModel:
    return InvestmentTypeModel(
      id=data.get("id"),
      created_at=str(data.get("created_at")),
      updated_at=str(data.get("updated_at")),
      name=data.get("name"),
      code=data.get("code"),
      color=data.get("color"),
    )
