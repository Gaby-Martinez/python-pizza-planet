from flask import Blueprint, jsonify, request

from app.common.http_methods import GET
from app.controllers.report import ReportController
from app.repositories.reports.report_strategy import (
    MonthWithMostRevenueStrategy,
    MostRequestedIngredientStrategy,
    TopCustomersStrategy,
)

report = Blueprint("report", __name__)


@report.route("/", methods=GET)
def generate_report():
    """Default: all reports. Query param 'type: 'most_requested_ingredient', 'month_with_most_revenue', 'top_customers'."""

    report_type = request.args.get("type")

    strategies = {
        "most_requested_ingredient": MostRequestedIngredientStrategy(),
        "month_with_most_revenue": MonthWithMostRevenueStrategy(),
        "top_customers": TopCustomersStrategy(),
    }

    report_controller = ReportController()

    if report_type:
        strategy = strategies.get(report_type)
        if not strategy:
            return jsonify({"error": "Invalid report type specified"}), 400
        report_controller.set_strategy(strategy)
        report_data = {report_type: report_controller.generate_report()}
    else:
        reports = {}
        for report_name, strategy in strategies.items():
            report_controller.set_strategy(strategy)
            reports[report_name] = report_controller.generate_report()
        report_data = reports

    return jsonify(report_data)
