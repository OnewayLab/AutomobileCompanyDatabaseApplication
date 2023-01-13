import json
import os
from random import choice, sample, randint

from . import db
from .models import *


def import_test_data(
    brand_models_path: str,
    customers_path: str,
    dealers_path: str,
    plants_path: str,
    suppliers_path: str,
    etc_path: str,
):
    """Import test data generated from json files

    Args:
        each arg is a json file path
    """
    brand_model_l = json.load(open(brand_models_path, "r"))
    customer_l = json.load(open(customers_path, "r"))
    dealer_l = json.load(open(dealers_path, "r"))
    plant_l = json.load(open(plants_path, "r"))
    supplier_l = json.load(open(suppliers_path, "r"))
    etc = json.load(open(etc_path, "r"))
    color_l, engine_l, transmission_l, part_l, vin_l, body_style_l = etc

    brands = []
    models = []
    options = []
    parts = []
    suppliers = []
    plants = []
    vehicles = []
    dealers = []
    customers = []

    # insert brands, models and options
    mid = 0
    for bid, brand in enumerate(brand_model_l):
        brand = Brand(bid=bid, name=brand)
        brands.append(brand)
        db.session.add(brand)
        # # insert models of this brand
        # for model in brand_model_l[brand]:
        #     model = Model(mid=mid, name=model, body_style=choice(body_style_l), bid=bid)
        #     models.append(model)
        #     db.session.add(model)
        #     # insert options of this model
        #     for i in range(randint(1, 5)):  # each model has 1-5 options
        #         option = Option(
        #             mid=mid,
        #             color=choice(color_l),
        #             engine=choice(engine_l),
        #             transmission=choice(transmission_l),
        #         )
        #         options.append(option)
        #         db.session.add(option)
            # # insert parts required by this model
            # for part_name in parts:
            #     part = Part(part_name + str(randint(1, 50)), part_name, "")
            #     parts.append(part)
            #     db.session.add(part)

            # mid += 1

    # insert parts

