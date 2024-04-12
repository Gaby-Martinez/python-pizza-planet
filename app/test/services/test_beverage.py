from app.test.utils.functions import get_random_price, get_random_string


def test_create_beverage_service(client, beverage_uri, beverage):
    response = client.post(beverage_uri, json=beverage)
    assert response.status_code == 201
    created_beverage = response.json
    assert "_id" in created_beverage
    assert created_beverage["name"] == beverage["name"]
    assert created_beverage["price"] == beverage["price"]


def test_update_beverage_service(client, create_beverage, beverage_uri):
    current_beverage = create_beverage.json
    _id = current_beverage["_id"]
    update_data = {"name": get_random_string(), "price": get_random_price(1, 5)}
    response = client.put(f"{beverage_uri}{_id}", json=update_data)
    assert response.status_code == 200
    updated_beverage = response.json
    for param, value in update_data.items():
        assert updated_beverage[param] == value


def test_get_beverage_by_id_service(client, create_beverage, beverage_uri):
    current_beverage = create_beverage.json
    response = client.get(f'{beverage_uri}{current_beverage["_id"]}')
    assert response.status_code == 200
    returned_beverage = response.json
    assert returned_beverage == current_beverage


def test_get_beverages_service(client, create_beverages, beverage_uri):
    response = client.get(beverage_uri)
    assert response.status_code == 200
    returned_beverages = {beverage["_id"]: beverage for beverage in response.json}
    for beverage in create_beverages:
        _id = beverage["_id"]
        assert _id in returned_beverages
        assert returned_beverages[_id]["name"] == beverage["name"]
        assert returned_beverages[_id]["price"] == beverage["price"]
