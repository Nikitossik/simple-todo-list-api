from app.models import User, Todo, db
from faker import Faker
from werkzeug.security import generate_password_hash
from datetime import timedelta

fake = Faker()

users = [
    User(email="first@gmail.com", password_hash=generate_password_hash("123123")),
    User(email="second@gmail.com", password_hash=generate_password_hash("123123")),
]


def populate_db():
    for user in users:
        db.session.add(user)

    for i in range(101):
        created_at = fake.date_time_this_month()  # random creation date in this month
        updated_at = fake.date_time_between_dates(
            datetime_start=created_at, datetime_end=created_at + timedelta(days=1)
        )  # random date of updating 1 day within

        db.session.add(
            Todo(
                title=fake.text(max_nb_chars=20),
                created_at=created_at,
                updated_at=updated_at,
                status=fake.random_element(elements=["todo", "in-progress", "done"]),
                user=fake.random_element(elements=users),
            )
        )

    db.session.commit()
