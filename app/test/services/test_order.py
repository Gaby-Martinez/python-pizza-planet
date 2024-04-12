import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_create_order_service(create_order):
    order = create_order.json
    assert create_order.status_code == 201
    assert "client_address" in order
    assert "client_dni" in order
    assert "client_name" in order
    assert "client_phone" in order
    assert "date" in order
    assert "size" in order
    assert "beverages" in order
    assert "ingredients" in order


def test_get_order_by_id_service(client, create_order, order_uri):
    current_order = create_order.json
    response = client.get(f'{order_uri}{current_order["_id"]}')
    assert response.status_code == 200
    returned_order = response.json
    for key, value in current_order.items():
        assert returned_order[key] == value


def test_get_orders_service(client, create_orders, order_uri):
    response = client.get(order_uri)
    assert response.status_code == 200
    returned_orders = {order["_id"]: order for order in response.json}
    create_order_ids = [order.json["_id"] for order in create_orders]
    for order_id in create_order_ids:
        assert order_id in returned_orders
