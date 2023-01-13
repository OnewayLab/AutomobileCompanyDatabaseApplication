from . import db


# length of strings
NAME_LEN = 40
INFO_LEN = 100


class Brand(db.Model):
    bid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_LEN), nullable=False, unique=True)

class Model(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_LEN), nullable=False)
    body_style = db.Column(db.String(INFO_LEN), nullable=False)
    bid = db.Column(db.Integer, db.ForeignKey("brand.bid", ondelete="CASCADE"), nullable=False)
    parts = db.relationship("Part", backref="models", secondary="requires")

class Option(db.Model):
    mid = db.Column(db.Integer, db.ForeignKey("model.mid", ondelete="CASCADE"), primary_key=True)
    color = db.Column(db.String(INFO_LEN), primary_key=True)
    engine = db.Column(db.String(INFO_LEN), primary_key=True)
    transmission = db.Column(db.String(INFO_LEN), primary_key=True)

class Part(db.Model):
    part_model = db.Column(db.String(NAME_LEN), primary_key=True)
    name = db.Column(db.String(NAME_LEN), nullable=False)
    info = db.Column(db.String(INFO_LEN))

class Supplier(db.Model):
    supplier_name = db.Column(db.String(NAME_LEN), primary_key=True)
    country = db.Column(db.String(NAME_LEN))
    city = db.Column(db.String(NAME_LEN))
    street = db.Column(db.String(NAME_LEN))
    parts = db.relationship("Part", backref="suppliers", secondary="supplies")

class Plant(db.Model):
    plant_name = db.Column(db.String(NAME_LEN), primary_key=True)
    work_type = db.Column(db.String(NAME_LEN), nullable=False)
    country = db.Column(db.String(NAME_LEN))
    city = db.Column(db.String(NAME_LEN))
    street = db.Column(db.String(NAME_LEN))

class Vehicle(db.Model):
    vin = db.Column(db.String(NAME_LEN), primary_key=True)
    price = db.Column(db.Float, nullable=False)
    plant_name = db.Column(db.String(NAME_LEN), db.ForeignKey("plant.plant_name"), nullable=False)
    assembly_date = db.Column(db.Date, nullable=False)
    mid = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(INFO_LEN), nullable=False)
    engine = db.Column(db.String(INFO_LEN), nullable=False)
    transmission = db.Column(db.String(INFO_LEN), nullable=False)
    db.ForeignKeyConstraint(["mid", "color", "engine", "transmission"], ["option.mid", "option.color", "option.engine", "option.transmission"])

class Dealer(db.Model):
    did = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_LEN), nullable=False, unique=True)
    country = db.Column(db.String(NAME_LEN))
    city = db.Column(db.String(NAME_LEN))
    brands = db.relationship("Brand", backref="dealers", secondary="sells")

class Customer(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_LEN), nullable=False)
    country = db.Column(db.String(NAME_LEN))
    city = db.Column(db.String(NAME_LEN))
    street = db.Column(db.String(NAME_LEN))
    gender = db.Column(db.String(NAME_LEN))
    annual_income = db.Column(db.Float)

class CustomerPhone(db.Model):
    cid = db.Column(db.Integer, db.ForeignKey("customer.cid", ondelete="CASCADE"), primary_key=True)
    phone = db.Column(db.String(NAME_LEN), primary_key=True)

class MadeOf(db.Model):
    vin = db.Column(db.String(NAME_LEN), db.ForeignKey("vehicle.vin", ondelete="CASCADE"), primary_key=True)
    part_model = db.Column(db.String(NAME_LEN), db.ForeignKey("part.part_model"), primary_key=True)
    manufacturer = db.Column(db.String(NAME_LEN))
    date = db.Column(db.Date, nullable=False)

class Inventory(db.Model):
    vin = db.Column(db.String(NAME_LEN), db.ForeignKey("vehicle.vin"), primary_key=True)
    did = db.Column(db.Integer, db.ForeignKey("dealer.did"), primary_key=True)
    date = db.Column(db.Date, nullable=False)
    is_sold = db.Column(db.Boolean, nullable=False)
    db.CheckConstraint("did IN (SELECT did FROM dealer, sells WHERE dealer.did = sells.did AND sells.bid = (SELECT bid FROM vehicle, model WHERE vehicle.mid = model.mid AND vehicle.vin = :vin))")

class Sales(db.Model):
    bid = db.Column(db.Integer, db.ForeignKey("brand.bid"), primary_key=True)
    mid = db.Column(db.Integer, db.ForeignKey("model.mid"), primary_key=True)
    color = db.Column(db.String(INFO_LEN), primary_key=True)
    did = db.Column(db.Integer, db.ForeignKey("dealer.did"), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    db.CheckConstraint(quantity >= 0)
    db.CheckConstraint("color in (select color from option where mid = model.mid)")

class Deal(db.Model):
    vin = db.Column(db.String(NAME_LEN), db.ForeignKey("vehicle.vin"), primary_key=True)
    did = db.Column(db.Integer, db.ForeignKey("dealer.did"), primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey("customer.cid"), primary_key=True)
    date = db.Column(db.Date, primary_key=True)

class Requires(db.Model):
    mid = db.Column(db.Integer, db.ForeignKey("model.mid", ondelete="CASCADE"), primary_key=True)
    part_model = db.Column(db.String(NAME_LEN), db.ForeignKey("part.part_model"), primary_key=True)

class Supplies(db.Model):
    supplier_name = db.Column(db.String(NAME_LEN), db.ForeignKey("supplier.supplier_name", ondelete="CASCADE"), primary_key=True)
    part_model = db.Column(db.String(NAME_LEN), db.ForeignKey("part.part_model"), primary_key=True)

class Manufactures(db.Model):
    plant_name = db.Column(db.String(NAME_LEN), db.ForeignKey("plant.plant_name", ondelete="CASCADE"), primary_key=True)
    part_model = db.Column(db.String(NAME_LEN), db.ForeignKey("part.part_model"), primary_key=True)

class Sells(db.Model):
    did = db.Column(db.Integer, db.ForeignKey("dealer.did", ondelete="CASCADE"), primary_key=True)
    bid = db.Column(db.Integer, db.ForeignKey("brand.bid", ondelete="CASCADE"), primary_key=True)

class QueryRecord(db.Model):
    bid = db.Column(db.Integer, db.ForeignKey("brand.bid"), primary_key=True)
    mid = db.Column(db.Integer, db.ForeignKey("model.mid"), primary_key=True)
    color = db.Column(db.String(INFO_LEN), primary_key=True)
    engine = db.Column(db.String(INFO_LEN), primary_key=True)
    transmission = db.Column(db.String(INFO_LEN), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    count = db.Column(db.Integer, nullable=False)