import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_get_sizes_service(client, create_sizes, size_uri):
    response = client.get(size_uri)
    pytest.assume(response.status.startswith("200"))
    returned_sizes = {size["_id"]: size for size in response.json}
    for ingredient in create_sizes:
        pytest.assume(ingredient["_id"] in returned_sizes)
