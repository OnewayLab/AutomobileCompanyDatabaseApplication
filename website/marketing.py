from flask import Blueprint, flash, session, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from datetime import date

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
    error = None

    today = date.today()
    years = [y for y in range(today.year - 10, today.year + 1)]
    months = [m for m in range(1, 13)]

    if request.method == "GET":
        session["begin_year"] = today.year - 10
        session["begin_month"] = 1
        session["end_year"] = today.year
        session["end_month"] = today.month
    else:
        session["begin_year"] = int(request.form["begin_year"])
        session["begin_month"] = int(request.form["begin_month"])
        session["end_year"] = int(request.form["end_year"])
        session["end_month"] = int(request.form["end_month"])

    query = (
        db.session.query(
            Dealer.did,
            Dealer.name,
            Dealer.country,
            Dealer.city,
            db.func.sum(Sales.quantity).label("quantity"),
            db.func.sum(Sales.sales).label("sales"),
        )
        .join(Sales)
        .filter(Sales.date >= f"{session['begin_year']}-{session['begin_month']}-01")
        .filter(Sales.date <= f"{session['end_year']}-{session['end_month']}-31")
        .group_by(Dealer.did)
    )
    result = query.all()

    if error:
        flash(error)

    return render_template("marketing/bydealer.html", result=result, years=years, months=months)


@bp.route("/bycustomer", methods=("GET", "POST"))
@login_required
def bycustomer():
    pass
