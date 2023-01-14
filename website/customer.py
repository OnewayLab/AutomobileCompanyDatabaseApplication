from flask import Blueprint, flash, session, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from database import db
from database.models import *
from modules.vehicle_locator import get_vehicles

from .auth import login_required
from .vehicle_shop import vehicle_shop

bp = Blueprint("customer", __name__, url_prefix="/customer")


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    return vehicle_shop()
