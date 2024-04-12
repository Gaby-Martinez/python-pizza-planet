from flask import Blueprint, jsonify, request

from app.common.http_methods import GET, POST, PUT
from app.services.base import BaseService

from ..controllers import SizeController

size = Blueprint("size", __name__)
size_service = BaseService(SizeController)


@size.route("/", methods=GET)
def get_sizes():
    return size_service.get_all()


@size.route("/<int:_id>", methods=GET)
def get_size_by_id(_id: int):
    return size_service.get_by_id(_id)


@size.route("/", methods=POST)
def create_size():
    return size_service.create(request.json)


@size.route("/<int:_id>", methods=PUT)
def update_size(_id: int):
    return size_service.update(_id, request.json)
