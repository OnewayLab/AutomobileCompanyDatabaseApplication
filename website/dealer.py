from flask import Blueprint, flash, session, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from database import db
from database.models import *
from modules.vehicle_locator import get_vehicles

from .auth import login_required
from .vehicle_shop import vehicle_shop


bp = Blueprint("dealer", __name__, url_prefix="/dealer")


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    error = None
    # get analysis type
    if request.method == "POST":
        if "type" in request.form:
            if request.form["type"] == "vehicle":
                return redirect(url_for("dealer.vehicles"))
            elif request.form["type"] == "inventory":
                return redirect(url_for("dealer.inventory"))
            else:
                error = "Invalid form."
        else:
            error = "Invalid form."
    if error:
        flash(error)
    return render_template("dealer/index.html")


@bp.route("/vehicles", methods=("GET", "POST"))
@login_required
def vehicles():
    return vehicle_shop()


@bp.route("/inventory", methods=("GET", "POST"))
@login_required
def inventory():
    did = Dealer.query.filter_by(name=session["username"]).first().did
    results = db.session.query(
        Inventory.vin,
        Inventory.date,
        Inventory.is_sold,
        Vehicle.plant_name,
        Vehicle.assembly_date,
        Vehicle.color,
        Vehicle.engine,
        Vehicle.transmission,
        Model.name.label("model"),
        Brand.name.label("brand"),
    ).select_from(Inventory).join(Vehicle, Model, Brand).filter(Inventory.did == did).all()
    return render_template("dealer/inventory.html", results=results)
