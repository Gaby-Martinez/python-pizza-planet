import pytest

from ..utils.functions import shuffle_list, get_random_sequence, get_random_string


def client_data_mock() -> dict:
    return {
        "client_address": get_random_string(),
        "client_dni": get_random_sequence(),
        "client_name": get_random_string(),
        "client_phone": get_random_sequence(),
    }


@pytest.fixture
def order_uri():
    return "/order/"


@pytest.fixture
def client_data():
    return client_data_mock()


@pytest.fixture
def create_orders(
    client, order_uri, create_ingredients, create_sizes, create_beverages
) -> list:
    ingredients = [ingredient.get("_id") for ingredient in create_ingredients]
    beverages = [beverage.get("_id") for beverage in create_beverages]
    sizes = [size.get("_id") for size in create_sizes]
    orders = []
    for _ in range(10):
        new_order = client.post(
            order_uri,
            json={
                **client_data_mock(),
                "ingredients": shuffle_list(ingredients)[:5],
                "beverages": shuffle_list(beverages)[:5],
                "size_id": shuffle_list(sizes)[0],
            },
        )
        orders.append(new_order)
    return orders


@pytest.fixture
def create_order(
    client, order_uri, create_ingredients, create_sizes, create_beverages
) -> dict:
    ingredients = [ingredient.get("_id") for ingredient in create_ingredients]
    beverages = [beverage.get("_id") for beverage in create_beverages]
    sizes = [size.get("_id") for size in create_sizes]
    response = client.post(
        order_uri,
        json={
            **client_data_mock(),
            "ingredients": shuffle_list(ingredients)[:5],
            "beverages": shuffle_list(beverages)[:5],
            "size_id": shuffle_list(sizes)[0],
        },
    )
    return response


@pytest.fixture
def order_data():
    return {
        "ingredients": [
            {"name": "Ingredient 1", "price": 10.0},
            {"name": "Ingredient 2", "price": 15.0},
        ],
        "beverages": [
            {"name": "Beverage 1", "price": 5.0},
            {"name": "Beverage 2", "price": 8.0},
        ],
        "size": {"name": "Large", "price": 20.0},
        "client_data": {
            "client_name": "John Doe",
            "client_dni": "12345678",
            "client_address": "123 Main St",
            "client_phone": "123456789",
        },
    }
