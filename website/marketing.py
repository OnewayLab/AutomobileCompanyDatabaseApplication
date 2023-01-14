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
    error = None

    today = date.today()
    end_year = today.year

    if request.method == "GET":
        session["byyear_begin_year"] = session["bymonth_begin_year"] = today.year - 10
        session["bymonth_begin_month"] = 1
        session["byyear_end_year"] = session["bymonth_end_year"] = today.year
        session["bymonth_end_month"] = today.month
    else:
        if request.form["by"] == "year":
            session["byyear_begin_year"] = int(request.form["begin_year"])
            session["byyear_end_year"] = int(request.form["end_year"])
        else:
            session["bymonth_begin_year"] = int(request.form["begin_year"])
            session["bymonth_begin_month"] = int(request.form["begin_month"])
            session["bymonth_end_year"] = int(request.form["end_year"])
            session["bymonth_end_month"] = int(request.form["end_month"])

    result_byyear = (
        db.session.query(
            db.extract("year", Sales.date).label("year"),
            db.func.sum(Sales.quantity).label("quantity"),
            db.func.sum(Sales.sales).label("sales"),
        )
        .filter(Sales.date >= f"{session['byyear_begin_year']}-01-01")
        .filter(Sales.date <= f"{session['byyear_end_year']}-12-31")
        .group_by("year")
        .all()
    )

    result_bymonth = (
        db.session.query(
            db.extract("year", Sales.date).label("year"),
            db.extract("month", Sales.date).label("month"),
            db.func.sum(Sales.quantity).label("quantity"),
            db.func.sum(Sales.sales).label("sales"),
        )
        .filter(
            Sales.date
            >= f"{session['bymonth_begin_year']}-{session['bymonth_begin_month']}-01"
        )
        .filter(
            Sales.date
            <= f"{session['bymonth_end_year']}-{session['bymonth_end_month']}-31"
        )
        .group_by("year", "month")
        .all()
    )

    if error:
        flash(error)

    return render_template(
        "marketing/bytime.html",
        end_year=end_year,
        result_byyear=result_byyear,
        result_bymonth=result_bymonth,
    )


@bp.route("/byvehicle", methods=("GET", "POST"))
@login_required
def byvehicle():
    pass


@bp.route("/bydealer", methods=("GET", "POST"))
@login_required
def bydealer():
    error = None

    today = date.today()
    end_year = today.year

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

    return render_template(
        "marketing/bydealer.html", end_year=end_year, result=result
    )


@bp.route("/bycustomer", methods=("GET", "POST"))
@login_required
def bycustomer():
    pass
