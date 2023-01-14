from flask import Blueprint, flash, session, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from database import db
from database.models import *
from modules.vehicle_locator import get_vehicles

from .auth import login_required


bp = Blueprint("customer", __name__, url_prefix="/customer")


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    error = None
    # get user selected items
    if request.method == "GET":
        session["selected_brand"] = None
        session["selected_model"] = None
        session["selected_color"] = None
        session["selected_engine"] = None
        session["selected_transmission"] = None
    else:
        if "brand" in request.form:
            brand_name = request.form["brand"]
            if brand_name == "any":
                session["selected_brand"] = None
            else:
                selected_brand = Brand.query.filter_by(name=brand_name).first()
                session["selected_brand"] = {"bid": selected_brand.bid, "name": selected_brand.name}
        elif "model" in request.form:
            model_name = request.form["model"]
            if model_name == "any":
                session["selected_model"] = None
            else:
                selected_model= Model.query.filter_by(
                    bid=session["selected_brand"]["bid"], name=model_name
                ).first()
                session["selected_model"] = {"mid": selected_model.mid, "name": selected_model.name}
        elif "color" in request.form:
            color = request.form["color"]
            session["selected_color"] = color if color != "any" else None
        elif "engine" in request.form:
            engine = request.form["engine"]
            session["selected_engine"] = engine if engine != "any" else None
        elif "transmission" in request.form:
            transmission = request.form["transmission"]
            session["selected_transmission"] = transmission if transmission != "any" else None
        else:
            error = "Invalid form."

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
    print(f"get vehicles with: {session['selected_brand']}, {session['selected_model']}, {session['selected_color']}, {session['selected_engine']}, {session['selected_transmission']}")
    vehicles = get_vehicles(
        session["selected_brand"]["bid"] if session["selected_brand"] else None,
        session["selected_model"]["mid"] if session["selected_model"] else None,
        session["selected_color"],
        session["selected_engine"],
        session["selected_transmission"],
    )

    if not error:
        return render_template(
            "customer/index.html",
            brands=brand_names,
            models=model_names,
            colors=colors,
            engines=engines,
            transmissions=transmissions,
            vehicles=vehicles,
        )
    else:
        flash(error)
        return render_template("customer/index.html")
