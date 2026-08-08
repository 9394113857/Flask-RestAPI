from flask import Blueprint, jsonify, request

from app.services.mobile_service import (
    add_mobile,
    delete_mobile,
    get_all_mobiles,
    get_mobile_by_id,
    update_mobile,
)


mobile_bp = Blueprint(
    "mobile",
    __name__,
    url_prefix="/mobiles",
)


# ============================================================
# GET ALL MOBILES
# ============================================================

@mobile_bp.route("", methods=["GET"])
def get_mobiles():
    mobiles = get_all_mobiles()

    if not mobiles:
        return jsonify(
            {
                "message": "No data available",
            }
        ), 200

    return jsonify(
        [
            mobile.to_dict()
            for mobile in mobiles
        ]
    ), 200


# ============================================================
# GET MOBILE BY ID
# ============================================================

@mobile_bp.route("/<int:id>", methods=["GET"])
def get_mobile_by_id_route(id):
    mobile = get_mobile_by_id(id)

    if not mobile:
        return jsonify(
            {
                "message": "Resource not found",
            }
        ), 404

    return jsonify(mobile.to_dict()), 200


# ============================================================
# CREATE MOBILE
# ============================================================

@mobile_bp.route("", methods=["POST"])
def create_mobile():
    data = request.get_json()

    if not data:
        return jsonify(
            {
                "message": "No data provided",
            }
        ), 400

    required_fields = [
        "name",
        "price",
        "ram",
        "storage",
    ]

    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "error": f"Missing field: {field}",
                }
            ), 400

    mobile = add_mobile(
        name=data["name"],
        price=data["price"],
        ram=data["ram"],
        storage=data["storage"],
    )

    if mobile is None:
        return jsonify(
            {
                "error": "Mobile already exists",
            }
        ), 400

    return jsonify(
        {
            "message": "Mobile added successfully",
            "mobile": mobile.to_dict(),
        }
    ), 201


# ============================================================
# UPDATE MOBILE
# ============================================================

@mobile_bp.route("/<int:id>", methods=["PUT"])
def update_mobile_route(id):
    data = request.get_json()

    if not data:
        return jsonify(
            {
                "message": "No data provided",
            }
        ), 400

    mobile = get_mobile_by_id(id)

    if not mobile:
        return jsonify(
            {
                "message": "Resource not found",
            }
        ), 404

    required_fields = [
        "name",
        "price",
        "ram",
        "storage",
    ]

    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "error": f"Missing field: {field}",
                }
            ), 400

    updated_mobile = update_mobile(
        mobile=mobile,
        name=data["name"],
        price=data["price"],
        ram=data["ram"],
        storage=data["storage"],
    )

    return jsonify(
        {
            "message": "Mobile updated successfully",
            "mobile": updated_mobile.to_dict(),
        }
    ), 200


# ============================================================
# DELETE MOBILE
# ============================================================

@mobile_bp.route("/<int:id>", methods=["DELETE"])
def delete_mobile_route(id):
    mobile = get_mobile_by_id(id)

    if not mobile:
        return jsonify(
            {
                "message": "Resource not found",
            }
        ), 404

    delete_mobile(mobile)

    return jsonify(
        {
            "message": "Mobile deleted successfully",
        }
    ), 200