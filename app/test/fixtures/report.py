import pytest
from unittest.mock import patch


@pytest.fixture
def report_url():
    return "/report/"


@pytest.fixture
def most_requested_ingredient_report():
    return {"name": "Tomato", "total": 150}


@pytest.fixture
def month_with_most_revenue_report():
    return {"month": "March 2024", "revenue": 20000}


@pytest.fixture
def top_customers_report():
    return [
        {"client_name": "John Doe", "total_spent": 300.0},
        {"client_name": "Jane Doe", "total_spent": 200.0},
        {"client_name": "Bob Smith", "total_spent": 150.0},
    ]


@pytest.fixture
def mocked_most_requested_ingredient_strategy(most_requested_ingredient_report):
    with patch(
        "app.controllers.utils.report_strategy.MostRequestedIngredientStrategy.generate",
        return_value=most_requested_ingredient_report,
    ) as mock:
        yield mock


@pytest.fixture
def mocked_month_with_most_revenue_strategy(month_with_most_revenue_report):
    with patch(
        "app.controllers.utils.report_strategy.MonthWithMostRevenueStrategy.generate",
        return_value=month_with_most_revenue_report,
    ) as mock:
        yield mock


@pytest.fixture
def mocked_top_customers_strategy(top_customers_report):
    with patch(
        "app.controllers.utils.report_strategy.TopCustomersStrategy.generate",
        return_value=top_customers_report,
    ) as mock:
        yield mock
