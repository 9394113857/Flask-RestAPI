from app.extensions import db
from app.models.mobile import Mobile


def get_all_mobiles():
    return Mobile.query.all()


def get_mobile_by_id(mobile_id):
    return db.session.get(Mobile, mobile_id)


def add_mobile(name, price, ram, storage):
    existing_mobile = Mobile.query.filter_by(
        name=name,
        price=price,
        ram=ram,
        storage=storage,
    ).first()

    if existing_mobile:
        return None

    mobile = Mobile(
        name=name,
        price=price,
        ram=ram,
        storage=storage,
    )

    db.session.add(mobile)
    db.session.commit()

    return mobile


def update_mobile(mobile, name, price, ram, storage):
    mobile.name = name
    mobile.price = price
    mobile.ram = ram
    mobile.storage = storage

    db.session.commit()

    return mobile


def delete_mobile(mobile):
    db.session.delete(mobile)
    db.session.commit()