from decorators.authentication import login_required, admin_required, seller_required
from flask import Blueprint, jsonify, request, render_template, session, url_for, flash, redirect
from controllers import home
import controllers.home

home_router = Blueprint('home_router', __name__)


@home_router.route('/add_home', methods=["POST", "GET"])
def add_home():
    if request.method == "POST":
        return controllers.home.add_home()
    return render_template("home/add_home_for_owner.html")


@home_router.route('/load_home', methods=["POST", "GET"])
@seller_required
def load_home():
    return controllers.home.load_home()


@home_router.route('/load_room', methods=["POST", "GET"])
@seller_required
def load_room():
    return controllers.home.load_room()


@home_router.route('/add_room', methods=["Get", "POST"])
def add_room():
    home_id = request.args.get('home_id')
    if home_id == None:
        return redirect(url_for('home_router.load_home'))
    if request.method == "POST":
        return controllers.home.add_room()
    return render_template("home/add_room.html", home_id=home_id)


@home_router.route('/info/<int:id>', methods=["GET"])
def info(id):
    return controllers.home.info(id)

@home_router.route('/')
def list_home():
    return controllers.home.list_home()


@home_router.route('/view_room_detail', methods=["GET"])
@login_required
def view_rooms_detail():
    home_id = request.args.get('home_id')
    return controllers.home.view_rooms_detail(home_id)


@home_router.route('/report/<int:home_id>', methods=["GET", "POST"])
def report(home_id, home_name):

    if request.method == "POST":
        return controllers.home.report(
            id,
            request.form.get("reason"),
            session.get("user_id"),
        )
    return render_template("report.html", home_id=home_id, home_name=home_name, reasons=reasons)


@home_router.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST" and request.form.get("home_name") != None:
        return controllers.home.search(request.form.get("home_name"))
    return render_template("home/search_home.html")


@home_router.route('/compare', methods=["GET", "POST"])
def compare():
    if request.method == "POST":
        if request.form.get("home1") != None and request.form.get("home2") != None:
            return controllers.home.compare(request.form.get("home1"), request.form.get("home2"))
        else:
            return redirect(url_for('home_router.list_home'))
    return render_template("compare_home.html")

