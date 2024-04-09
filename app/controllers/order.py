from sqlalchemy.exc import SQLAlchemyError

from ..common.utils import check_required_keys
from ..repositories.managers import (
    BeverageManager,
    IngredientManager,
    OrderManager,
    SizeManager,
)
from .base import BaseController


class OrderController(BaseController):
    manager = OrderManager
    __required_info = (
        "client_name",
        "client_dni",
        "client_address",
        "client_phone",
        "size_id",
    )

    @staticmethod
    def calculate_order_price(size_price: float, ingredients: list, beverages: list):
        ingredient_prices = sum(ingredient.price for ingredient in ingredients)
        beverage_prices = sum(beverage.price for beverage in beverages)
        total_price = ingredient_prices + size_price + beverage_prices
        return round(total_price, 2)

    @classmethod
    def create(cls, order: dict):
        current_order = order.copy()

        if not check_required_keys(cls.__required_info, current_order):
            return None, "Invalid order payload"

        size_id = current_order.get("size_id")
        size = SizeManager.get_by_id(size_id)
        if not size:
            return None, "Invalid size for Order"

        ingredient_ids = current_order.pop("ingredients", [])
        beverage_ids = current_order.pop("beverages", [])

        try:
            ingredients = (
                IngredientManager.get_by_id_list(ingredient_ids)
                if ingredient_ids
                else []
            )
            beverages = (
                BeverageManager.get_by_id_list(beverage_ids) if beverage_ids else []
            )

            total_price = cls.calculate_order_price(
                size.get("price", 0), ingredients, beverages
            )
            order_with_price = {**current_order, "total_price": total_price}

            created_order = cls.manager.create(order_with_price, ingredients, beverages)
            return created_order, None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
