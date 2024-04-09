from app.controllers import IngredientController, OrderController, SizeController
from app.controllers.base import BaseController
from app.controllers.beverage import BeverageController


def __order(order_data: dict):
    ingredient_ids = [ingredient["_id"] for ingredient in order_data["ingredients"]]
    beverage_ids = [beverage["_id"] for beverage in order_data["beverages"]]
    size_id = order_data["size"]["_id"]
    return {
        **order_data["client_data"],
        "ingredients": ingredient_ids,
        "beverages": beverage_ids,
        "size_id": size_id,
    }


def __create_items(items: list, controller: BaseController):
    created_items = []
    for item in items:
        created_item, _ = controller.create(item)
        created_items.append(created_item)
    return created_items


def __create_sizes_ingredients_and_beverages(order_data: dict):
    created_ingredients = __create_items(
        order_data["ingredients"], IngredientController
    )
    created_beverages = __create_items(order_data["beverages"], BeverageController)
    created_size, _ = SizeController.create(order_data["size"])
    return created_size, created_ingredients, created_beverages


def test_create(app, order_data: dict):
    created_size, created_ingredients, created_beverages = (
        __create_sizes_ingredients_and_beverages(order_data)
    )

    order_data["ingredients"] = created_ingredients
    order_data["beverages"] = created_beverages
    order_data["size"] = created_size

    order = __order(order_data)
    created_order, error = OrderController.create(order)

    size_id = order.pop("size_id", None)
    ingredient_ids = order.pop("ingredients", [])
    beverage_ids = order.pop("beverages", [])

    assert error is None
    for param, value in order.items():
        assert param in created_order
        assert value == created_order[param]

    assert created_order["_id"]
    assert size_id == created_order["size"]["_id"]

    ingredients_in_detail = set(
        item["ingredient"]["_id"] for item in created_order["ingredients"]
    )
    assert not ingredients_in_detail.difference(ingredient_ids)

    beverages_in_detail = set(
        item["beverage"]["_id"] for item in created_order["beverages"]
    )
    assert not beverages_in_detail.difference(beverage_ids)


def test_calculate_order_price(app, order_data: dict):
    created_size, created_ingredients, created_beverages = (
        __create_sizes_ingredients_and_beverages(order_data)
    )
    order_data["ingredients"] = created_ingredients
    order_data["beverages"] = created_beverages
    order_data["size"] = created_size
    order = __order(order_data)
    created_order, _ = OrderController.create(order)
    assert created_order["total_price"] == round(
        created_size["price"]
        + sum(ingredient["price"] for ingredient in created_ingredients)
        + sum(beverage["price"] for beverage in created_beverages),
        2,
    )


def test_get_by_id(app, order_data: dict):
    created_size, created_ingredients, created_beverages = (
        __create_sizes_ingredients_and_beverages(order_data)
    )
    order_data["ingredients"] = created_ingredients
    order_data["beverages"] = created_beverages
    order_data["size"] = created_size
    order = __order(order_data)
    created_order, _ = OrderController.create(order)
    order_from_db, error = OrderController.get_by_id(created_order["_id"])
    size_id = order.pop("size_id", None)
    ingredient_ids = order.pop("ingredients", [])
    beverage_ids = order.pop("beverages", [])
    assert error is None
    for param, value in created_order.items():
        assert order_from_db[param] == value
    assert size_id == created_order["size"]["_id"]

    ingredients_in_detail = set(
        item["ingredient"]["_id"] for item in created_order["ingredients"]
    )
    assert not ingredients_in_detail.difference(ingredient_ids)

    beverages_in_detail = set(
        item["beverage"]["_id"] for item in created_order["beverages"]
    )
    assert not beverages_in_detail.difference(beverage_ids)


def test_get_all(app, order_data: dict):
    created_size, created_ingredients, created_beverages = (
        __create_sizes_ingredients_and_beverages(order_data)
    )
    created_orders = []
    for _ in range(5):
        order_data["ingredients"] = created_ingredients
        order_data["beverages"] = created_beverages
        order_data["size"] = created_size
        order = __order(order_data)
        created_order, _ = OrderController.create(order)
        created_orders.append(created_order)

    orders_from_db, error = OrderController.get_all()
    searchable_orders = {db_order["_id"]: db_order for db_order in orders_from_db}
    assert error is None
    for created_order in created_orders:
        current_id = created_order["_id"]
        assert current_id in searchable_orders
        for param, value in created_order.items():
            assert searchable_orders[current_id][param] == value
