from typing import Any, Dict, Tuple, Type

from flask import jsonify


class BaseService:
    def __init__(self, controller: Type):
        self.controller = controller

    def get_all(self) -> Tuple[Dict[str, Any], int]:
        entities, error = self.controller.get_all()
        response = entities if not error else {"error": error}
        status_code = 200 if entities else 404 if not error else 400
        return jsonify(response), status_code

    def get_by_id(self, _id: int) -> Tuple[Dict[str, Any], int]:
        entity, error = self.controller.get_by_id(_id)
        response = entity if not error else {"error": error}
        status_code = 200 if entity else 404 if not error else 400
        return jsonify(response), status_code

    def create(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        entity, error = self.controller.create(data)
        response = entity if not error else {"error": error}
        status_code = 201 if not error else 400
        return jsonify(response), status_code

    def update(self, _id: int, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        entity, error = self.controller.update(_id, data)
        response = entity if not error else {"error": error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code
