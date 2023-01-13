import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from database import db


bp = Blueprint("auth", __name__)


@bp.before_app_request
def load_logged_in_user():
    username = session.get("username")

    if username is None:
        g.user = None
    else:
        g.user = {"username": session["username"], "role": session["role"]}


@bp.route("/", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        role = request.form["role"]
        username = request.form["username"]
        password = request.form["password"]
        error = None
        # user = db.execute(
        #     "SELECT * FROM user WHERE username = ?", (username,)
        # ).fetchone()

        # if user is None:
        #     error = "Incorrect username."
        # elif not check_password_hash(user["password"], password):
        #     error = "Incorrect password."

        if error is None:
            session.clear()
            session["username"] = username
            session["role"] = role
            if role == "customer":
                print(f"customer {username} login")
                return redirect(url_for("customer.index"))
            elif role == "dealer":
                print(f"dealer {username} login")
                return redirect(url_for("dealer.index"))
            elif role == "supplier":
                print(f"marketing {username} login")
                return redirect(url_for("marketing.index"))
            else:
                error = "Incorrect role."

        flash(error)

    return render_template("auth/login.html")


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
