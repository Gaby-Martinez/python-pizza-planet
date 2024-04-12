from unittest.mock import MagicMock

import pytest

from app.controllers.report import ReportController
from app.repositories.reports.report_strategy import (
    MonthWithMostRevenueStrategy,
    MostRequestedIngredientStrategy,
    TopCustomersStrategy,
)


def test_generate_report_with_most_requested_ingredient_strategy(
    most_requested_ingredient_report,
):
    mock_strategy = MagicMock(spec=MostRequestedIngredientStrategy)
    expected_report = most_requested_ingredient_report
    mock_strategy.generate.return_value = expected_report

    controller = ReportController()
    controller.set_strategy(mock_strategy)

    assert controller.generate_report() == expected_report
    mock_strategy.generate.assert_called_once()


def test_generate_report_with_month_with_most_revenue_strategy(
    month_with_most_revenue_report,
):
    mock_strategy = MagicMock(spec=MonthWithMostRevenueStrategy)
    expected_report = month_with_most_revenue_report
    mock_strategy.generate.return_value = expected_report

    controller = ReportController()
    controller.set_strategy(mock_strategy)

    assert controller.generate_report() == expected_report
    mock_strategy.generate.assert_called_once()


def test_generate_report_with_top_customers_strategy(top_customers_report):
    mock_strategy = MagicMock(spec=TopCustomersStrategy)
    expected_report = top_customers_report
    mock_strategy.generate.return_value = expected_report

    controller = ReportController()
    controller.set_strategy(mock_strategy)

    assert controller.generate_report() == expected_report
    mock_strategy.generate.assert_called_once()


def test_generate_report_no_strategy():
    controller = ReportController()
    message, status_code = controller.generate_report()
    assert message == "No strategy selected"
    assert status_code == 400


def test_generate_report_strategy_exception():
    mock_strategy = MagicMock(spec=MonthWithMostRevenueStrategy)
    mock_strategy.generate.side_effect = Exception("Error generating report")

    controller = ReportController()
    controller.set_strategy(mock_strategy)

    with pytest.raises(Exception) as excinfo:
        controller.generate_report()
    assert str(excinfo.value) == "Error generating report"
