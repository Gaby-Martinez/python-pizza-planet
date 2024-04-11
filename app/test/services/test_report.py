import pytest


@pytest.mark.parametrize(
    "report_type, expected_mock",
    [
        ("most_requested_ingredient", "mocked_most_requested_ingredient_strategy"),
        ("month_with_most_revenue", "mocked_month_with_most_revenue_strategy"),
        ("top_customers", "mocked_top_customers_strategy"),
    ],
)
def test_generate_specific_report_service(
    client,
    report_url,
    report_type,
    expected_mock,
    mocked_most_requested_ingredient_strategy,
    mocked_month_with_most_revenue_strategy,
    mocked_top_customers_strategy,
    most_requested_ingredient_report,
    month_with_most_revenue_report,
    top_customers_report,
):
    mock_mapping = {
        "mocked_most_requested_ingredient_strategy": mocked_most_requested_ingredient_strategy,
        "mocked_month_with_most_revenue_strategy": mocked_month_with_most_revenue_strategy,
        "mocked_top_customers_strategy": mocked_top_customers_strategy,
    }
    expected_data = {
        "most_requested_ingredient": most_requested_ingredient_report,
        "month_with_most_revenue": month_with_most_revenue_report,
        "top_customers": top_customers_report,
    }

    url = f"{report_url}?type={report_type}"
    response = client.get(url)

    assert response.status_code == 200
    data = response.get_json()

    for mock_name, mock in mock_mapping.items():
        if mock_name == expected_mock:
            mock.assert_called_once()
            assert data == {report_type: expected_data[report_type]}
        else:
            mock.assert_not_called()
