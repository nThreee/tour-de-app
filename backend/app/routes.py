from typing import Any, TypedDict

from flask import Blueprint, jsonify, request
from sqlalchemy import select

from .extensions import db
from .models import Product, Name

product_bp = Blueprint("products", __name__)
health_bp = Blueprint("health", __name__)

class ProductData(TypedDict):
    name: str
    cost: int

class NameData(TypedDict):
    name: str
    team: str

def extract_product() -> ProductData | None:
    data: dict[str, Any] = request.get_json(silent=True) or {}  # pyright: ignore[reportExplicitAny]
    if data.get("name") is None or data.get("cost") is None:
        return None

    return {"name": data["name"], "cost": data["cost"]}

def extract_name() -> NameData | None:
    data: dict[str, str] = request.get_json(silent=True) or {}  # pyright: ignore[reportExplicitAny]
    if data.get("name") is None or data.get("team") is None:
        return None

    return {"name": data["name"], "team": data["team"]}    

@product_bp.get("")
def list_products():
    products = db.session.scalars(select(Product).order_by(Product.id)).all()
    return jsonify([product.to_dict() for product in products]), 200

@product_bp.get("/names")
def list_names():
    names = db.session.scalars(select(Name)).all()
    return jsonify([name.to_dict() for name in names]), 200

@product_bp.post("/names")
def create_names():
    data = extract_name()
    if data is None:
        return jsonify({"message": "name and team are required"}), 400

    name = Name()
    name.name = data["name"]
    name.team = data["team"]
    db.session.add(name)
    db.session.commit()

    return jsonify(name.to_dict()), 200

@product_bp.post("")
def create_product():
    data = extract_product()
    if data is None:
        return jsonify({"message": "name and cost are required"}), 400

    product = Product()
    product.name = data["name"]
    product.cost = data["cost"]
    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 200


@product_bp.put("/<int:product_id>")
def update_product(product_id: int):
    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify({"message": "Product does not exist"}), 404

    data = extract_product()
    if data is None:
        return jsonify({"message": "name and cost are required"}), 400

    product.name = data["name"]
    product.cost = data["cost"]
    db.session.commit()

    return jsonify(product.to_dict()), 200


@product_bp.delete("/<int:product_id>")
def delete_product(product_id: int):
    product = db.session.get(Product, product_id)
    if product is not None:
        db.session.delete(product)
        db.session.commit()

    return jsonify({"message": "Product was deleted permanently from DB."}), 200

@health_bp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200
