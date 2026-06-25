from __core.plugins.cache.memory import Memory
from __core.plugins.database.sql.sqlite import SQLite
from __core.repository import Repository

from app.models import InvestmentRentabilityModel

class InvestmentRentabilityRepository(Repository):
  def __init__(self):
    self.__table = "investment_rentabilities"
    self.__database = SQLite()
    self.__cache = Memory()

  def find(self) -> list[InvestmentRentabilityModel]:
    data = self.__cache.read_json("InvestmentRentabilityRepository::find")
    if data:
      return data

    results = self.__database.select(self.__table, {})
    data = [InvestmentRentabilityRepository.__format(item) for item in results]
    self.__cache.write_json("InvestmentRentabilityRepository::find", data)
    return data

  @staticmethod
  def __format(data: dict) -> InvestmentRentabilityModel:
    return InvestmentRentabilityModel(
      id=data.get("id"),
      created_at=str(data.get("created_at")),
      updated_at=str(data.get("updated_at")),
      name=data.get("name"),
    )
