import json
import os
import random
from random import choice, sample, randint
from radar import random_date
from flask import Flask

from . import db
from .models import *


def import_test_data(
    app: Flask,
    brand_models_path: str,
    customers_path: str,
    dealers_path: str,
    plants_path: str,
    suppliers_path: str,
    etc_path: str,
):
    """Import test data generated from json files

    Args:
        app: Flask app
        other args are json file paths of test data sources
    """
    random.seed(1234)
    brand_models = json.load(open(brand_models_path, "r"))
    customers = json.load(open(customers_path, "r"))
    dealers = json.load(open(dealers_path, "r"))
    plants = json.load(open(plants_path, "r"))
    suppliers = json.load(open(suppliers_path, "r"))
    etc = json.load(open(etc_path, "r"))
    colors, engines, transmissions, parts, vins, body_styles = etc.values()

    max_mid = 0
    generated_parts = set()
    assembly_plant = set()
    generated_options = {}
    generated_requires = {}
    part_manufacturers = {}
    generated_sells = {}
    generated_inventory = []
    generated_customers = []

    def add(obj):
        db.session.add(obj)
        db.session.commit()

    with app.app_context():
        # objects to be inserted
        # insert brands, models and options
        for bid, brand in enumerate(brand_models):
            b = Brand(bid=bid, name=brand)
            add(b)
            # insert models of this brand
            for model in brand_models[brand]:
                m = Model(
                    mid=max_mid, name=model, body_style=choice(body_styles), bid=bid
                )
                add(m)
                # insert options of this model
                option_set = set()
                for _ in range(randint(1, 5)):  # each model has 1-5 options
                    op = (choice(colors), choice(engines), choice(transmissions))
                    if op not in option_set:
                        option_set.add(op)
                        option = Option(
                            mid=max_mid,
                            color=op[0],
                            engine=op[1],
                            transmission=op[2],
                        )
                        add(option)
                generated_options[max_mid] = option_set
                # insert parts required by this model
                generated_requires[max_mid] = set()
                for part_name in parts:
                    p = (part_name + str(randint(1, 50)), part_name)
                    if p not in generated_parts:
                        generated_parts.add(p)
                        part = Part(
                            part_model=p[0],
                            name=p[1],
                            info="",
                        )
                        db.session.add(part)
                    r = Requires(mid=max_mid, part_model=p[0])
                    generated_requires[max_mid].add(p)
                    add(r)
                max_mid += 1
        max_mid -= 1

        # insert suppliers
        for supplier in suppliers:
            s = Supplier(
                supplier_name=supplier["name"],
                country=supplier["country"],
                city=supplier["city"],
                street=supplier["street"],
            )
            add(s)
            for part in sample(generated_parts, randint(1, 5)):
                ss = Supplies(
                    supplier_name=supplier["name"],
                    part_model=part[0],
                )
                add(ss)
                if part[0] not in part_manufacturers:
                    part_manufacturers[part[0]] = set()
                part_manufacturers[part[0]].add(supplier["name"])

        # insert plants
        for plant in plants:
            p = Plant(
                plant_name=plant["name"],
                work_type=plant["work_type"],
                country=plant["country"],
                city=plant["city"],
                street=plant["street"],
            )
            add(p)
            if plant["work_type"] == "assembly":
                assembly_plant.add(plant["name"])
            else:
                for part in sample(generated_parts, randint(1, 5)):
                    pp = Manufactures(
                        plant_name=plant["name"],
                        part_model=part[0],
                    )
                    add(pp)
                    if part[0] not in part_manufacturers:
                        part_manufacturers[part[0]] = set()
                    part_manufacturers[part[0]].add(plant["name"])

        # insert dealers
        for dealer in dealers:
            d = Dealer(
                did=dealer["did"],
                name=dealer["name"],
                country=dealer["country"],
                city=dealer["city"],
            )
            add(d)
            for bid in sample(range(len(brand_models)), randint(1, len(brand_models)/2)):
                dd = Sells(did=dealer["did"], bid=bid)
                add(dd)
                if bid not in generated_sells:
                    generated_sells[bid] = set()
                generated_sells[bid].add(dealer["did"])

        # insert customers
        for customer in customers:
            c = Customer(
                cid=customer["cid"],
                name=customer["name"],
                country=customer["country"],
                city=customer["city"],
                street=customer["street"],
                gender=customer["gender"],
                annual_income=customer["annual_income"],
            )
            add(c)
            generated_customers.append(customer)
            for phone in customer["phone"]:
                cp = CustomerPhone(
                    cid=customer["cid"],
                    phone=phone,
                )
                add(cp)

        # insert vehicles
        for vin in vins:
            plant = choice(list(assembly_plant))
            date = random_date()
            mid = randint(0, max_mid)
            color, engine, transmission = choice(list(generated_options[mid]))
            v = Vehicle(
                vin=vin,
                price=randint(10000, 100000),
                plant_name=plant,
                assembly_date=date,
                mid=mid,
                color=color,
                engine=engine,
                transmission=transmission,
            )
            add(v)
            # insert made_of
            for part in generated_requires[mid]:
                # 从 suppliers 和 manufactures 中随机选择一个制造商
                if part[0] in part_manufacturers:
                    manufacturer = choice(list(part_manufacturers[part[0]]))
                else:
                    manufacturer = "unknown"
                made_of = MadeOf(
                    vin=vin,
                    part_model=part[0],
                    manufacturer=manufacturer,
                    date=random_date(stop=date),
                )
                add(made_of)
            # insert inventory
            bid = Model.query.filter_by(mid=mid).first().bid
            if bid not in generated_sells:
                continue
            did = choice(list(generated_sells[bid]))
            inventory = Inventory(
                vin=vin,
                did=did,
                date=random_date(start=date),
                is_sold=randint(0, 1),
            )
            add(inventory)
            generated_inventory.append(inventory)

        # insert deal
        for inventory in sample(
            generated_inventory, randint(0, int(len(generated_inventory) / 2))
        ):
            inventory.is_sold = 1
            deal = Deal(
                vin=inventory.vin,
                did=inventory.did,
                cid=choice(generated_customers)["cid"],
                date=random_date(start=inventory.date),
            )
            vehicle = Vehicle.query.filter_by(vin=inventory.vin).first()
            bid = Model.query.filter_by(mid=vehicle.mid).first().bid
            add(deal)
            sales = Sales.query.filter_by(
                bid=bid,
                mid=vehicle.mid,
                color=vehicle.color,
                did=inventory.did,
                date=deal.date,
            ).first()
            if sales:
                sales.quantity += 1
            else:
                sales = Sales(
                    bid=bid,
                    mid=vehicle.mid,
                    color=vehicle.color,
                    did=inventory.did,
                    date=deal.date,
                    quantity=1,
                )
                add(sales)