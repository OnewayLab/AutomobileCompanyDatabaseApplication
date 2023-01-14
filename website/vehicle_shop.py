from flask import Blueprint, flash, session, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from database import db
from database.models import *
from modules.vehicle_locator import get_vehicles


def vehicle_shop():
    # get user selected items
    if request.method == "GET":
        session["selected_brand"] = None
        session["selected_model"] = None
        session["selected_color"] = None
        session["selected_engine"] = None
        session["selected_transmission"] = None
    else:
        if "forDealers" in request.form:
            dealers = get_vehicles(
                mid=Model.query.filter_by(name=request.form["model"]).first().mid,
                color=request.form["color"],
                engine=request.form["engine"],
                transmission=request.form["transmission"],
                is_sold=False,
                select=[Dealer],
            )
            message = f"售卖该车型的经销商有：{', '.join([dealer.name for dealer in dealers])}"
            flash(message)
        else:
            if request.form["brand"] == "any":
                session["selected_brand"] = None
            else:
                selected_brand = Brand.query.filter_by(name=request.form["brand"]).first()
                session["selected_brand"] = {
                    "bid": selected_brand.bid,
                    "name": selected_brand.name,
                }
            if request.form["model"] == "any" or request.form["brand"] == "any":
                session["selected_model"] = None
            else:
                selected_model = Model.query.filter_by(
                    bid=session["selected_brand"]["bid"], name=request.form["model"]
                ).first()
                session["selected_model"] = {
                    "mid": selected_model.mid,
                    "name": selected_model.name,
                }
            color = request.form["color"]
            session["selected_color"] = color if color != "any" else None
            engine = request.form["engine"]
            session["selected_engine"] = engine if engine != "any" else None
            transmission = request.form["transmission"]
            session["selected_transmission"] = (
                transmission if transmission != "any" else None
            )

    # get brand names
    brands = Brand.query.all()
    brand_names = [brand.name for brand in brands]

    # get model names
    if session["selected_brand"]:
        models = Model.query.filter_by(bid=session["selected_brand"]["bid"]).all()
        model_names = list({model.name for model in models})
    else:
        model_names = []

    # get options
    if session["selected_model"]:
        options = Option.query.filter_by(mid=session["selected_model"]["mid"]).all()
    else:
        options = Option.query.all()
    colors = list({option.color for option in options})
    engines = list({option.engine for option in options})
    transmissions = list({option.transmission for option in options})

    # get vehicles
    print(
        f"get vehicles with: {session['selected_brand']}, {session['selected_model']}, {session['selected_color']}, {session['selected_engine']}, {session['selected_transmission']}"
    )
    results = get_vehicles(
        session["selected_brand"]["bid"] if session["selected_brand"] else None,
        session["selected_model"]["mid"] if session["selected_model"] else None,
        session["selected_color"],
        session["selected_engine"],
        session["selected_transmission"],
        select=[
            Brand.name.label("brand"),
            Model.name.label("model"),
            Option.color,
            Option.engine,
            Option.transmission,
            Option.price,
            db.func.count(Vehicle.vin).label("stock"),
        ],
        group_by=[
            Brand.name,
            Model.name,
            Option.color,
            Option.engine,
            Option.transmission,
            Option.price,
        ],
    )

    return render_template(
        "customer/index.html",
        brands=brand_names,
        models=model_names,
        colors=colors,
        engines=engines,
        transmissions=transmissions,
        results=results,
    )
