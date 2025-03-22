from __core.plugins.cache.memory import Memory
from __core.plugins.database.sql.postgresql import PostgreSQL
from __core.repository import Repository

from app.models import InvestmentSourceModel

class InvestmentSourceRepository(Repository):
  def __init__(self):
    self.__table = "investment_sources"
    self.__database = PostgreSQL()
    self.__cache = Memory()

  def find(self) -> list[InvestmentSourceModel]:
    data = self.__cache.read_json("InvestmentSourceRepository::find")
    if data:
      return data

    results = self.__database.select(self.__table, {})
    data = [InvestmentSourceRepository.__format(item) for item in results]
    self.__cache.write_json("InvestmentSourceRepository::find", data)
    return data

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
