from flask import Blueprint, request

from app.common.http_methods import GET, POST, PUT
from app.services.base import BaseService

from ..controllers import BeverageController

beverage = Blueprint("beverage", __name__)
beverage_service = BaseService(BeverageController)


@beverage.route("/", methods=GET)
def get_beverages():
    return beverage_service.get_all()


@beverage.route("/<int:_id>", methods=GET)
def get_beverage_by_id(_id: int):
    return beverage_service.get_by_id(_id)


@beverage.route("/", methods=POST)
def create_beverage():
    return beverage_service.create(request.json)


@beverage.route("/<int:_id>", methods=PUT)
def update_beverage(_id: int):
    return beverage_service.update(_id, request.json)
