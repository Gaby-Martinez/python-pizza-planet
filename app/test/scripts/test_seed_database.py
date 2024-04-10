import pytest

from app.common.scripts.seed_database import (
    create_beverages,
    create_ingredients,
    create_orders,
    create_sizes,
)
from app.repositories.models import (
    Beverage,
    Ingredient,
    Order,
    OrderBeverage,
    OrderIngredient,
    Size,
)


@pytest.fixture
def data_generator(app):
    with app.app_context():
        yield app


def test_create_sizes(data_generator):
    with data_generator.app_context():
        create_sizes()
        assert Size.query.count() == 5


def test_create_ingredients(data_generator):
    with data_generator.app_context():
        create_ingredients()
        assert Ingredient.query.count() == 10


def test_create_beverages(data_generator):
    with data_generator.app_context():
        create_beverages()
        assert Beverage.query.count() == 5


def test_create_orders(data_generator):
    with data_generator.app_context():
        create_sizes()
        create_ingredients()
        create_beverages()
        create_orders(num_orders=10)

        assert Order.query.count() == 10
        assert OrderIngredient.query.count() > 0
        assert OrderBeverage.query.count() > 0


def test_data_generation(data_generator):
    with data_generator.app_context():
        create_sizes()
        create_ingredients()
        create_beverages()
        create_orders(num_orders=10)

        assert Size.query.count() == 5
        assert Ingredient.query.count() == 10
        assert Beverage.query.count() == 5
        assert Order.query.count() == 10
        assert OrderIngredient.query.count() > 0
        assert OrderBeverage.query.count() > 0
