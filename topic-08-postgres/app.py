"""
Flask application for pets database using PostgreSQL
Adapted from Topic 4 SQLite version
"""

from flask import Flask, render_template, request, redirect, url_for
import os
import database

app = Flask(__name__)

# Initialize with environment variables (secure!)
database.initialize(
    host=os.environ.get('POSTGRES_HOST', 'localhost'),
    database=os.environ.get('POSTGRES_DB', 'pets_db'),
    user=os.environ.get('POSTGRES_USER', 'pets_app'),
    password=os.environ.get('POSTGRES_PASSWORD')
)


@app.route("/", methods=["GET"]) 
@app.route("/list", methods=["GET"])
def get_list():
    """Display list of all pets"""
    pets = database.get_pets()
    return render_template("list.html", pets=pets)


@app.route("/kind", methods=["GET"])
@app.route("/kind/list", methods=["GET"])
def get_kind_list():
    """Display list of all pet kinds"""
    kinds = database.get_kinds()
    return render_template("kind_list.html", kinds=kinds)


@app.route("/create", methods=["GET"])
def get_create():
    """Show create pet form"""
    kinds = database.get_kinds()
    return render_template("create.html", kinds=kinds)


@app.route("/create", methods=["POST"])
def post_create():
    """Create a new pet"""
    data = dict(request.form)
    database.create_pet(data)
    return redirect(url_for("get_list"))


@app.route("/delete/<id>", methods=["GET"])
def get_delete(id):
    """Delete a pet"""
    database.delete_pet(id)
    return redirect(url_for("get_list"))


@app.route("/update/<id>", methods=["GET"])
def get_update(id):
    """Show update pet form"""
    data = database.get_pet(id)
    kinds = database.get_kinds()
    return render_template("update.html", data=data, kinds=kinds)


@app.route("/update/<id>", methods=["POST"])
def post_update(id):
    """Update a pet"""
    data = dict(request.form)
    database.update_pet(id, data)
    return redirect(url_for("get_list"))


@app.route("/kind/create", methods=["GET"])
def get_kind_create():
    """Show create kind form"""
    return render_template("kind_create.html")


@app.route("/kind/create", methods=["POST"])
def post_kind_create():
    """Create a new kind"""
    data = dict(request.form)
    database.create_kind(data)
    return redirect(url_for("get_kind_list"))


@app.route("/kind/delete/<id>", methods=["GET"])
def get_kind_delete(id):
    """Delete a kind"""
    try:
        database.delete_kind(id)
    except Exception as e:
        return render_template("error.html", error_text=str(e))
    return redirect(url_for("get_kind_list"))


@app.route("/kind/update/<id>", methods=["GET"])
def get_kind_update(id):
    """Show update kind form"""
    data = database.get_kind(id)
    return render_template("kind_update.html", data=data)


@app.route("/kind/update/<id>", methods=["POST"])
def post_kind_update(id):
    """Update a kind"""
    data = dict(request.form)
    database.update_kind(id, data)
    return redirect(url_for("get_kind_list"))


if __name__ == "__main__":
    app.run(debug=True)
