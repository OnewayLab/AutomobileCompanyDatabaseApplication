from flask import (
    Flask,
    flash,
    render_template,
    request,
)
from tmp.database import MysqlDb

# MySQL配置
MYSQL_HOST = "127.0.0.1"  # 表示本地的地址
MYSQL_PORT = 3306  # 端口号
MYSQL_USER = "root"  # 用户名
MYSQL_PASSWD = "891568935"  # 密码
MYSQL_DB = "university"  # 数据库名称


app = Flask(__name__, template_folder="./")
app.secret_key = "dev"
db = MysqlDb(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB)


def createDropDown(attributes):
    """
    生成下拉框
    """
    dropDown = ""
    for attribute in attributes:
        dropDown += f"<option value='{attribute}'>{attribute}</option>"
    return dropDown


def createDropDownFromSQL(sql):
    """
    生成下拉框
    """
    dropDown = ""
    data = db.query(sql)
    for d in data:
        dropDown += (
            f"<option value='{list(d.values())[0]}'>{list(d.values())[0]}</option>"
        )
    return dropDown


@app.route("/")
def index():
    dropdown = createDropDownFromSQL("select distinct dept_name from department")
    return render_template("index.html", dropdown=dropdown)


@app.route("/insert-student", methods=["GET", "POST"])
def insert_student():
    """
    插入学生信息
    """
    print(request.form)
    dropdown = createDropDownFromSQL("select distinct dept_name from department")
    try:
        id = request.form["id"]
        name = request.form["name"]
        dept_name = request.form["dept_name"]
        db.execute(f"insert into student values ('{id}', '{name}', '{dept_name}', '0')")
        flash("插入成功")
    except Exception as e:
        flash(f"Error: {e}")
    return render_template("index.html", dropdown=dropdown)


@app.route("/insert-instructor", methods=["GET", "POST"])
def insert_instructor():
    """
    插入教师信息
    """
    print(request.form)
    dropdown = createDropDownFromSQL("select distinct dept_name from department")
    try:
        id = request.form["id"]
        name = request.form["name"]
        dept_name = request.form["dept_name"]
        salary = request.form["salary"]
        db.execute(
            f"insert into instructor values ('{id}', '{name}', '{dept_name}', '{salary}')"
        )
        flash("插入成功")
    except Exception as e:
        flash(f"Error: {e}")
    return render_template("index.html", dropdown=dropdown)


if __name__ == "__main__":
    app.run(debug=True, port=8888, host="127.0.0.1")
