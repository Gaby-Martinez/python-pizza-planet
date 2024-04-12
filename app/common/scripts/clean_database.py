import logging

from app import flask_app
from app.plugins import db
from app.repositories.models import (
    Beverage,
    Ingredient,
    Order,
    OrderBeverage,
    OrderIngredient,
    Size,
)

logging.basicConfig(level=logging.INFO)


def clean_database():
    """Deletes all records from specific tables in the database."""
    try:
        OrderIngredient.query.delete()
        OrderBeverage.query.delete()
        Order.query.delete()
        Ingredient.query.delete()
        Beverage.query.delete()
        Size.query.delete()

        db.session.commit()
        logging.info("Database cleaned successfully.")
    except Exception as e:
        logging.error(f"An error occurred while cleaning the database: {e}")
        db.session.rollback()


if __name__ == "__main__":
    with flask_app.app_context():
        confirm = input(
            "Are you sure you want to clean the database? This action cannot be undone. Type 'yes' to confirm: "
        )
        if confirm.lower() == "yes":
            clean_database()
        else:
            logging.info("Database cleaning canceled.")
