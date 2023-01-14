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
    print(request.path.rsplit("/", 1))
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
    error = None

    today = date.today()
    end_year = today.year

    # get user selected items
    if request.method == "GET":
        session["begin_year"] = end_year - 10
        session["begin_month"] = 1
        session["end_year"] = end_year
        session["end_month"] = today.month
        session["selected_brand"] = None
        session["selected_model"] = None
        session["selected_color"] = "any"
    else:
        session["begin_year"] = int(request.form["begin_year"])
        session["begin_month"] = int(request.form["begin_month"])
        session["end_year"] = int(request.form["end_year"])
        session["end_month"] = int(request.form["end_month"])
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
        options = Sales.query.filter_by(mid=session["selected_model"]["mid"]).all()
    else:
        options = Option.query.all()
    colors = list({option.color for option in options})

    group_by = []
    columns = []
    if session["selected_model"]:
        colors = (
            db.session.query(Sales.color)
            .filter_by(mid=session["selected_model"]["mid"])
            .distinct()
            .all()
        )
        group_by += [Brand.name, Model.name]
        columns += ["品牌", "车型"]
    elif session["selected_brand"]:
        colors = (
            db.session.query(Sales.color)
            .filter_by(bid=session["selected_brand"]["bid"])
            .distinct()
            .all()
        )
        group_by += [Brand.name]
        columns += ["品牌"]
    else:
        colors = db.session.query(Sales.color).distinct().all()
        group_by += [Sales.color]
        columns += ["颜色"]

    # get sales
    result = (
        db.session.query(
            db.func.sum(Sales.quantity).label("quantity"),
            db.func.sum(Sales.sales).label("sales"),
            *group_by,
        )
        .join(Brand, Model)
        .filter(Sales.date >= f"{session['begin_year']}-{session['begin_month']}-01")
        .filter(Sales.date <= f"{session['end_year']}-{session['end_month']}-31")
        .group_by(*group_by)
        .all()
    )

    if error:
        flash(error)

    return render_template(
        "marketing/byvehicle.html",
        end_year=end_year,
        brands=brand_names,
        models=model_names,
        colors=colors,
        results=result,
        columns=columns
    )


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

    return render_template("marketing/bydealer.html", end_year=end_year, result=result)


@bp.route("/bycustomer", methods=("GET", "POST"))
@login_required
def bycustomer():
    error = None

    today = date.today()
    end_year = today.year

    if request.method == "GET":
        session["bygender_begin_year"] = session["byincome_begin_year"] = (
            today.year - 10
        )
        session["bygender_begin_month"] = session["byincome_begin_month"] = 1
        session["bygender_end_year"] = session["byincome_end_year"] = today.year
        session["bygender_end_month"] = session["byincome_end_month"] = today.month
    else:
        type = request.form["by"]
        session["by" + type + "_begin_year"] = int(request.form["begin_year"])
        session["by" + type + "_begin_month"] = int(request.form["begin_month"])
        session["by" + type + "_end_year"] = int(request.form["end_year"])
        session["by" + type + "_end_month"] = int(request.form["end_month"])

    result_bygender = (
        db.session.query(
            Sales.customer_gender,
            db.func.sum(Sales.quantity).label("quantity"),
            db.func.sum(Sales.sales).label("sales"),
        )
        .filter(
            Sales.date
            >= f"{session['bygender_begin_year']}-{session['bygender_begin_month']}-01"
        )
        .filter(
            Sales.date
            <= f"{session['bygender_end_year']}-{session['bygender_end_month']}-31"
        )
        .group_by(Sales.customer_gender)
        .all()
    )

    result_byincome = (
        db.session.query(
            Sales.customer_income_range,
            db.func.sum(Sales.quantity).label("quantity"),
            db.func.sum(Sales.sales).label("sales"),
        )
        .filter(
            Sales.date
            >= f"{session['byincome_begin_year']}-{session['byincome_begin_month']}-01"
        )
        .filter(
            Sales.date
            <= f"{session['byincome_end_year']}-{session['byincome_end_month']}-31"
        )
        .group_by(Sales.customer_income_range)
        .all()
    )

    if error:
        flash(error)

    return render_template(
        "marketing/bycustomer.html",
        end_year=end_year,
        result_bygender=result_bygender,
        result_byincome=result_byincome,
    )
