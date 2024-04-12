from app.test.utils.functions import get_random_price, get_random_string


def test_create_ingredient_service(client, ingredient_uri, ingredient):
    response = client.post(ingredient_uri, json=ingredient)
    assert response.status_code == 201
    created_ingredient = response.json
    assert "_id" in created_ingredient
    assert created_ingredient["name"] == ingredient["name"]
    assert created_ingredient["price"] == ingredient["price"]


def test_update_ingredient_service(client, create_ingredient, ingredient_uri):
    current_ingredient = create_ingredient.json
    _id = current_ingredient["_id"]
    update_data = {"name": get_random_string(), "price": get_random_price(1, 5)}
    response = client.put(f"{ingredient_uri}{_id}", json=update_data)
    assert response.status_code == 200
    updated_ingredient = response.json
    for param, value in update_data.items():
        assert updated_ingredient[param] == value


def test_get_ingredient_by_id_service(client, create_ingredient, ingredient_uri):
    current_ingredient = create_ingredient.json
    response = client.get(f'{ingredient_uri}{current_ingredient["_id"]}')
    assert response.status_code == 200
    returned_ingredient = response.json
    assert returned_ingredient == current_ingredient


def test_get_ingredients_service(client, create_ingredients, ingredient_uri):
    response = client.get(ingredient_uri)
    assert response.status_code == 200
    returned_ingredients = {
        ingredient["_id"]: ingredient for ingredient in response.json
    }
    for ingredient in create_ingredients:
        _id = ingredient["_id"]
        assert _id in returned_ingredients
        assert returned_ingredients[_id]["name"] == ingredient["name"]
        assert returned_ingredients[_id]["price"] == ingredient["price"]
