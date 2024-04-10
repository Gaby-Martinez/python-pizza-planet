import random
from datetime import datetime, timedelta

from faker import Faker

from app import flask_app
from app.plugins import db
from app.repositories.models import (
    Beverage,
    Ingredient,
    Order,
    OrderBeverage,
    OrderIngredient,
    Size,
)

fake = Faker()


def generate_price(min_price: float, max_price: float, increment: float) -> float:
    total_increments = int((max_price - min_price) / increment) + 1
    random_increment = random.randint(0, total_increments - 1)
    return round(min_price + (random_increment * increment), 2)


def calculate_order_total_price(size_price, ingredient_ids, beverage_ids):
    ingredients_total = sum(Ingredient.query.get(id).price for id in ingredient_ids)
    beverages_total = sum(Beverage.query.get(id).price for id in beverage_ids)
    total_price = round(size_price + ingredients_total + beverages_total, 2)
    return total_price


def create_sizes():
    sizes = ["Small", "Medium", "Large", "Extra Large", "Family Size"]
    min_price = 5.0
    max_price = 30.0
    price_increment = (max_price - min_price) / (len(sizes) - 1)
    for index, size in enumerate(sizes):
        price = round(min_price + (price_increment * index), 2)
        db.session.add(Size(name=size, price=price))
    db.session.commit()


def create_ingredients():
    ingredients = [
        "Cheese",
        "Pepperoni",
        "Mushrooms",
        "Onions",
        "Sausage",
        "Bacon",
        "Black Olives",
        "Green Peppers",
        "Pineapple",
        "Spinach",
    ]
    for ingredient in ingredients:
        price = generate_price(0.5, 5.0, 0.25)
        db.session.add(Ingredient(name=ingredient, price=price))
    db.session.commit()


def create_beverages():
    beverages = ["Coke", "Wine", "Beer", "Water", "Lemonade"]
    for beverage in beverages:
        price = generate_price(1.0, 10.0, 0.5)
        db.session.add(Beverage(name=beverage, price=price))
    db.session.commit()


def create_orders(num_orders: int = 100):
    sizes = Size.query.all()
    ingredients = Ingredient.query.all()
    beverages = Beverage.query.all()
    customers = [
        (fake.unique.name(), fake.unique.random_number(digits=8, fix_len=True))
        for _ in range(20)
    ]

    for _ in range(num_orders):
        customer_name, customer_dni = random.choice(customers)

        month_offset = random.choice([-5, -4, -3, -2, -1, 0])
        today = datetime.now()
        start_date = today.replace(day=1) + timedelta(days=30 * month_offset)
        end_date = start_date + timedelta(days=30)
        order_date = fake.date_time_between_dates(
            datetime_start=start_date, datetime_end=end_date
        )

        selected_size = random.choice(sizes)
        selected_ingredients = random.sample(
            [ingredient._id for ingredient in ingredients], k=random.randint(1, 5)
        )
        selected_beverages = random.sample(
            [beverage._id for beverage in beverages], k=random.randint(1, 3)
        )

        total_price = calculate_order_total_price(
            selected_size.price, selected_ingredients, selected_beverages
        )

        order = Order(
            client_name=customer_name,
            client_dni=customer_dni,
            client_address=fake.address(),
            client_phone=fake.phone_number(),
            date=order_date,
            total_price=total_price,
            size_id=selected_size._id,
        )
        db.session.add(order)
        db.session.flush()

        for ingredient_id in selected_ingredients:
            ingredient = Ingredient.query.get(ingredient_id)
            db.session.add(
                OrderIngredient(
                    order_id=order._id,
                    ingredient_id=ingredient_id,
                    ingredient_price=ingredient.price,
                )
            )

        for beverage_id in selected_beverages:
            beverage = Beverage.query.get(beverage_id)
            db.session.add(
                OrderBeverage(
                    order_id=order._id,
                    beverage_id=beverage_id,
                    beverage_price=beverage.price,
                )
            )

    db.session.commit()


if __name__ == "__main__":
    with flask_app.app_context():
        db.create_all()
        create_sizes()
        create_ingredients()
        create_beverages()
        create_orders()
