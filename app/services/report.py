from flask import Blueprint, jsonify
from sqlalchemy.sql import extract, func

from app.common.http_methods import GET
from app.plugins import db
from app.repositories.models import Ingredient, Order, OrderIngredient
from app.repositories.serializers import OrderSerializer

report = Blueprint("report", __name__)


@report.route("/", methods=GET)
def generate_report():
    most_requested_ingredient = (
        db.session.query(
            Ingredient.name, func.count(OrderIngredient.ingredient_id).label("total")
        )
        .join(OrderIngredient)
        .group_by(Ingredient.name)
        .order_by(func.count(OrderIngredient.ingredient_id).desc())
        .first()
    )
    most_requested_ingredient = {
        "name": most_requested_ingredient[0],
        "total": most_requested_ingredient[1],
    }

    month_with_highest_revenue = (
        db.session.query(
            extract("month", Order.date).label("month"),
            func.sum(Order.total_price).label("revenue"),
        )
        .group_by("month")
        .order_by(func.sum(Order.total_price).desc())
        .first()
    )
    month_with_highest_revenue = {
        "month": month_with_highest_revenue[0],
        "revenue": float(month_with_highest_revenue[1]),
    }

    top_customers = (
        db.session.query(
            Order.client_name, func.sum(Order.total_price).label("total_spent")
        )
        .group_by(Order.client_name)
        .order_by(func.sum(Order.total_price).desc())
        .limit(3)
        .all()
    )

    top_customers = [
        {
            "client_name": customer.client_name,
            "total_spent": float(customer.total_spent),
        }
        for customer in top_customers
    ]

    report_data = {
        "most_requested_ingredient": most_requested_ingredient,
        "month_with_highest_revenue": month_with_highest_revenue,
        "top_customers": top_customers,
    }

    return jsonify(report_data)
