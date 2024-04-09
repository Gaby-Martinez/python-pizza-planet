from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column

from .models import (
    Beverage,
    Ingredient,
    Order,
    OrderBeverage,
    OrderIngredient,
    Size,
    db,
)
from .serializers import (
    BeverageSerializer,
    IngredientSerializer,
    OrderSerializer,
    SizeSerializer,
    ma,
)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return (
            cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        )


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return (
            cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        )


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(
        cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]
    ):
        try:
            new_order = cls.model(**order_data)
            cls.session.add(new_order)
            cls.session.flush()

            # Add ingredients to the order
            for ingredient in ingredients:
                cls.session.add(
                    OrderIngredient(
                        order_id=new_order._id,
                        ingredient_id=ingredient._id,
                        ingredient_price=ingredient.price,
                    )
                )

            # Add beverages to the order
            for beverage in beverages:
                cls.session.add(
                    OrderBeverage(
                        order_id=new_order._id,
                        beverage_id=beverage._id,
                        beverage_price=beverage.price,
                    )
                )

            cls.session.refresh(new_order)
            cls.session.commit()
            return cls.serializer().dump(new_order)
        except Exception as ex:
            cls.session.rollback()
            raise ex


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column("1")).from_statement(text("SELECT 1")).all()
