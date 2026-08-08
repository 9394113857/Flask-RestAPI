from app.extensions import db


class Mobile(db.Model):

    __tablename__ = "mobiles"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(255),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    ram = db.Column(
        db.String(50),
        nullable=False
    )

    storage = db.Column(
        db.String(50),
        nullable=False
    )

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "ram": self.ram,
            "storage": self.storage
        }