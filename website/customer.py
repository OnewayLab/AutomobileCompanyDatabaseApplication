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
    print(request.form)
    # get user selected items
    if request.method == "POST":
        if "brand" in request.form:
            brand_name = request.form["brand"]
            selected_brand = Brand.query.filter_by(name=brand_name).first()
            session["selected_brand"] = {"bid": selected_brand.bid, "name": selected_brand.name}
        elif "model" in request.form:
            model_name = request.form["model"]
            selected_model= Model.query.filter_by(
                bid=session["selected_brand"]["bid"], name=model_name
            ).first()
            session["selected_model"] = {"mid": selected_model.mid, "name": selected_model.name}
        elif "color" in request.form:
            color = request.form["color"]
            session["selected_color"] = color
        elif "engine" in request.form:
            engine = request.form["engine"]
            session["selected_engine"] = engine
        elif "transmission" in request.form:
            transmission = request.form["transmission"]
            session["selected_transmission"] = transmission
        else:
            error = "Invalid form."

    # get brand names
    brands = Brand.query.all()
    brand_names = [brand.name for brand in brands]
    if "selected_brand" not in session:
        session["selected_brand"] = {"bid": brands[0].bid, "name": brands[0].name}

    # get model names
    models = Model.query.filter_by(bid=session["selected_brand"]["bid"]).all()
    model_names = list({model.name for model in models})
    if "selected_model" not in session:
        session["selected_model"] = {"mid": models[0].mid, "name": models[0].name}

    # get options
    options = Option.query.filter_by(mid=session["selected_model"]["mid"]).all()
    colors = list({option.color for option in options})
    if "selected_color" not in session:
        session["selected_color"] = colors[0]
    engines = list({option.engine for option in options})
    if "selected_engine" not in session:
        session["selected_engine"] = engines[0]
    transmissions = list({option.transmission for option in options})
    if "selected_transmission" not in session:
        session["selected_transmission"] = transmissions[0]

    # get vehicles
    vehicles = get_vehicles(
        session["selected_brand"]["bid"],
        session["selected_model"]["mid"],
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
