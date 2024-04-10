from abc import ABC, abstractmethod

from sqlalchemy import func

from app.plugins import db
from app.repositories.models import Ingredient, Order, OrderIngredient


class ReportStrategy(ABC):
    @abstractmethod
    def generate(self):
        pass


class MostRequestedIngredientStrategy(ReportStrategy):
    def generate(self):
        result = (
            db.session.query(
                Ingredient.name,
                func.count(OrderIngredient.ingredient_id).label("total"),
            )
            .join(OrderIngredient)
            .group_by(Ingredient.name)
            .order_by(func.count(OrderIngredient.ingredient_id).desc())
            .first()
        )
        return {"name": result[0], "total": result[1]}


class MonthWithMostRevenueStrategy(ReportStrategy):

    MONTH_NAMES = {
        1: "January",
        2: "Febrraury",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    def generate(self):
        month, year, revenue = self._get_month_year_revenue()
        month_name = self.MONTH_NAMES[month]
        return {"month": f"{month_name} {year}", "revenue": revenue}

    def _get_month_year_revenue(self):
        result = (
            db.session.query(
                func.cast(func.strftime("%m", Order.date), db.Integer),
                func.strftime("%Y", Order.date),
                func.sum(Order.total_price),
            )
            .group_by(func.strftime("%m", Order.date), func.strftime("%Y", Order.date))
            .order_by(func.sum(Order.total_price).desc())
            .first()
        )
        return result


class TopCustomersStrategy(ReportStrategy):
    def generate(self):
        results = (
            db.session.query(
                Order.client_name, func.sum(Order.total_price).label("total_spent")
            )
            .group_by(Order.client_name)
            .order_by(func.sum(Order.total_price).desc())
            .limit(3)
            .all()
        )
        return [
            {"client_name": result[0], "total_spent": float(result[1])}
            for result in results
        ]
