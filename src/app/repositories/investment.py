from __core.plugins.cache.memory import Memory
from __core.plugins.database.sql.postgresql import PostgreSQL
from __core.repository import Repository

from app.models import (
  InvestmentModel,
  InvestmentRentabilityModel,
  InvestmentSourceModel,
  InvestmentTypeModel,
)

class InvestmentRepository(Repository):
  def __init__(self):
    self.__table = "investments"
    self.__database = PostgreSQL()
    self.__cache = Memory()

  def create(self, data: InvestmentModel) -> str:
    self.__database.insert(self.__table, data.to_dict())
    self.__cache.remove(["InvestmentRepository::consolidated"])
    return data.id

  def find(
    self,
    user_id: str,
    get_change_after_date: str = None,
    page: int = None,
    limit: int = None,
    order_by: str = None,
  ) -> list[InvestmentModel]:
    query = """
      SELECT
        main_table.*,
        COALESCE(
          (SELECT
             change
           FROM investment_changes
           WHERE
             investment_id = main_table.id AND
             created_at >= %(after_date)s
           ORDER BY
             created_at DESC
           LIMIT 1),
          0
        ) AS fk_change,
        fk_type.name AS fk_type_name,
        fk_type.code AS fk_type_code,
        fk_type.color AS fk_type_color,
        fk_source.name AS fk_source_name,
        fk_source.code AS fk_source_code,
        fk_source.logo AS fk_source_logo,
        fk_rentability.name AS fk_rentability_name
      FROM investments AS main_table
        INNER JOIN investment_types AS fk_type ON fk_type.id = type_id
        INNER JOIN investment_sources AS fk_source ON fk_source.id = source_id
        LEFT OUTER JOIN investment_rentabilities AS fk_rentability ON fk_rentability.id = rentability_id
      WHERE user_id = %(user_id)s
    """

    if order_by:
      query += f"ORDER BY {order_by} DESC, updated_at DESC"
    else:
      query += "ORDER BY updated_at DESC"

    if limit:
      query += f"\nLIMIT {limit}"

    if page and limit:
      query += f"\nOFFSET {(page - 1) * limit}"

    results = self.__database.query(query, {
      "after_date": get_change_after_date,
      "user_id": user_id,
    })
    return [InvestmentRepository.__format(item) for item in results]

  def consolidated(self, user_id: str, get_week_change_after_date: str) -> dict:
    data = self.__cache.read_json("InvestmentRepository::consolidated")
    if data:
      return data

    query = """
      SELECT
        COUNT(1),
        SUM(invested) AS invested,
        SUM(total) AS total,
        SUM(COALESCE(
          (SELECT
             change
           FROM investment_changes
           WHERE
             investment_id = main_table.id AND
             created_at >= %(after_week_start_date)s
           ORDER BY
             created_at DESC
           LIMIT 1),
          0
        )) AS week_gains
      FROM investments AS main_table
      WHERE
        user_id = %(user_id)s;
    """

    results = self.__database.query(query, {
      "after_week_start_date": get_week_change_after_date,
      "user_id": user_id,
    })
    data = results[0]
    self.__cache.write_json("InvestmentRepository::consolidated", data)
    return data

  def find_one(self, user_id: str, id: str) -> InvestmentModel | None:
    result = self.__database.select(self.__table, { "id": id, "user_id": user_id })
    return InvestmentRepository.__format(result[0]) if len(result) > 0 else None

  def update(self, user_id: str, id: str, new_data: InvestmentModel) -> None:
    self.__database.update(self.__table, { "id": id, "user_id": user_id }, new_data.to_dict())
    self.__cache.remove(["InvestmentRepository::consolidated"])

  def remove_one(self, user_id: str, id: str) -> None:
    self.__database.delete(self.__table, { "id": id, "user_id": user_id })
    self.__cache.remove(["InvestmentRepository::consolidated"])

  @staticmethod
  def __format(data: dict) -> InvestmentModel:
    return InvestmentModel(
      id=data.get("id"),
      created_at=str(data.get("created_at")),
      updated_at=str(data.get("updated_at")),
      user_id=data.get("user_id"),
      name=data.get("name"),
      invested=round(float(data.get("invested")), 2),
      total=round(float(data.get("total")), 2),
      maturity=str(data.get("maturity")) if data.get("maturity") else None,

      fk_change=round(float(data.get("fk_change")) if data.get("fk_change") else 0, 2),

      type_id=data.get("type_id"),
      fk_type=InvestmentTypeModel(
        name=data.get("fk_type_name"),
        code=data.get("fk_type_code"),
        color=data.get("fk_type_color"),
      ) if data.get("fk_type_code") and data.get("fk_type_color") else None,

      source_id=data.get("source_id"),
      fk_source=InvestmentSourceModel(
        name=data.get("fk_source_name"),
        code=data.get("fk_source_code"),
        logo=data.get("fk_source_logo") if data.get("fk_source_logo") else None,
      ),

      rentability_id=data.get("rentability_id"),
      rentability_number=round(float(data.get("rentability_number")), 2) if data.get("rentability_number") else None,
      fk_rentability=InvestmentRentabilityModel(
        name=data.get("fk_rentability_name"),
      ) if data.get("rentability_id") else None,
    )
