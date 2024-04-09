from datetime import datetime, timezone

from app.plugins import db


class Order(db.Model):
    __tablename__ = "orders"
    _id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(80))
    client_dni = db.Column(db.String(10))
    client_address = db.Column(db.String(128))
    client_phone = db.Column(db.String(15))
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    total_price = db.Column(db.Float)
    size_id = db.Column(db.Integer, db.ForeignKey("sizes._id"))

    size = db.relationship("Size", back_populates="orders")
    ingredients = db.relationship(
        "OrderIngredient", back_populates="order", cascade="all, delete-orphan"
    )
    beverages = db.relationship(
        "OrderBeverage", back_populates="order", cascade="all, delete-orphan"
    )


class Ingredient(db.Model):
    __tablename__ = "ingredients"
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    order_ingredients = db.relationship("OrderIngredient", back_populates="ingredient")


class Size(db.Model):
    __tablename__ = "sizes"
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    orders = db.relationship("Order", back_populates="size")


class OrderIngredient(db.Model):
    __tablename__ = "order_ingredients"
    _id = db.Column(db.Integer, primary_key=True)
    ingredient_price = db.Column(db.Float)
    order_id = db.Column(db.Integer, db.ForeignKey("orders._id"))
    ingredient_id = db.Column(
        db.Integer, db.ForeignKey("ingredients._id"), nullable=False
    )

    order = db.relationship("Order", back_populates="ingredients")
    ingredient = db.relationship("Ingredient", back_populates="order_ingredients")


class Beverage(db.Model):
    __tablename__ = "beverages"
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    order_beverages = db.relationship("OrderBeverage", back_populates="beverage")


class OrderBeverage(db.Model):
    __tablename__ = "order_beverages"
    _id = db.Column(db.Integer, primary_key=True)
    beverage_price = db.Column(db.Float)
    order_id = db.Column(db.Integer, db.ForeignKey("orders._id"))
    beverage_id = db.Column(db.Integer, db.ForeignKey("beverages._id"))

    order = db.relationship("Order", back_populates="beverages")
    beverage = db.relationship("Beverage", back_populates="order_beverages")
