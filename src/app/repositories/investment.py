from __core.plugins.cache.memory import Memory
from __core.plugins.database.sql.sqlite import SQLite
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
    self.__database = SQLite()
    self.__cache = Memory()

  def create(self, data: InvestmentModel) -> str:
    self.__database.insert(self.__table, data.to_dict())
    self.__cache.remove([f"InvestmentRepository::consolidated::{data.user_id}"])
    return data.id

  def create_batch(self, data: list[InvestmentModel]) -> None:
    self.__database.batch_insert(self.__table, "id", [item.to_dict() for item in data])

    user_id = data[0].user_id
    self.__cache.remove([f"InvestmentRepository::consolidated::{user_id}"])

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
             created_at >= :after_date
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
      WHERE user_id = :user_id
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

  def consolidated(self, user_id: str, start_of_week_date: str, start_of_month_date: str) -> dict:
    data = self.__cache.read_json(f"InvestmentRepository::consolidated::{user_id}")
    if data:
      return data

    query = """
      SELECT
        COUNT(1) AS count,
        SUM(invested) AS invested,
        SUM(total) AS total,
        SUM(COALESCE(
          (SELECT
             change
           FROM investment_changes
           WHERE
             investment_id = main_table.id AND
             created_at >= :start_of_month_date
           ORDER BY
             created_at DESC
           LIMIT 1),
          0
        )) AS monthly_gains,
        SUM(COALESCE(
          (SELECT
             change
           FROM investment_changes
           WHERE
             investment_id = main_table.id AND
             created_at >= :start_of_week_date
           ORDER BY
             created_at DESC
           LIMIT 1),
          0
        )) AS week_gains
      FROM investments AS main_table
      WHERE
        user_id = :user_id;
    """

    results = self.__database.query(query, {
      "start_of_week_date": start_of_week_date,
      "start_of_month_date": start_of_month_date,
      "user_id": user_id,
    })
    data = results[0]
    self.__cache.write_json(f"InvestmentRepository::consolidated::{user_id}", data)
    return data

  def find_one(self, user_id: str, id: str) -> InvestmentModel | None:
    result = self.__database.select(self.__table, { "id": id, "user_id": user_id })
    return InvestmentRepository.__format(result[0]) if len(result) > 0 else None

  def update(self, user_id: str, id: str, new_data: InvestmentModel) -> None:
    self.__database.update(self.__table, { "id": id, "user_id": user_id }, new_data.to_dict())
    self.__cache.remove([f"InvestmentRepository::consolidated::{user_id}"])

  def remove_one(self, user_id: str, id: str) -> None:
    self.__database.delete(self.__table, { "id": id, "user_id": user_id })
    self.__cache.remove([f"InvestmentRepository::consolidated::{user_id}"])

  @staticmethod
  def __format(data: dict) -> InvestmentModel:
    return InvestmentModel(
      id=data.get("id"),
      created_at=str(data.get("created_at")),
      updated_at=str(data.get("updated_at")),
      user_id=data.get("user_id"),
      name=data.get("name"),
      maturity=str(data.get("maturity")) if data.get("maturity") else None,
      invested=round(float(data.get("invested")), 2),
      total=round(float(data.get("total")), 2),

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
