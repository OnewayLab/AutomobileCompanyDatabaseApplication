from flask import Blueprint, flash, session, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from database import db
from database.models import *
from modules.vehicle_locator import get_vehicles

from .auth import login_required


bp = Blueprint("marketing", __name__, url_prefix="/marketing")


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    error = None

    # get analysis type
    if request.method == "POST":
        if "type" in request.form:
            if request.form["type"] == "time":
                return redirect(url_for("marketing.bytime"))
            elif request.form["type"] == "vehicle":
                return redirect(url_for("marketing.byvehicle"))
            elif request.form["type"] == "dealer":
                return redirect(url_for("marketing.bydealer"))
            elif request.form["type"] == "customer":
                return redirect(url_for("marketing.bycustomer"))
            else:
                error = "Invalid form."
        else:
            error = "Invalid form."

    if error:
        flash(error)

    return render_template("marketing/index.html")


@bp.route("/bytime", methods=("GET", "POST"))
@login_required
def bytime():
    pass


@bp.route("/byvehicle", methods=("GET", "POST"))
@login_required
def byvehicle():
    pass


@bp.route("/bydealer", methods=("GET", "POST"))
@login_required
def bydealer():
    pass


@bp.route("/bycustomer", methods=("GET", "POST"))
@login_required
def bycustomer():
    pass
