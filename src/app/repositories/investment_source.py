from __core.plugins.database.sql.postgresql import PostgreSQL
from __core.repository import Repository

from app.models import InvestmentSourceModel

class InvestmentSourceRepository(Repository):
  def __init__(self):
    self.__table = "investment_sources"
    self.__database = PostgreSQL()

  def find(self) -> list[InvestmentSourceModel]:
    results = self.__database.select(self.__table, {})
    return [InvestmentSourceRepository.__format(item) for item in results]

  @staticmethod
  def __format(data: dict) -> InvestmentSourceModel:
    return InvestmentSourceModel(
      id=data.get("id"),
      created_at=str(data.get("created_at")),
      updated_at=str(data.get("updated_at")),
      name=data.get("name"),
      code=data.get("code"),
      logo=data.get("logo"),
    )
