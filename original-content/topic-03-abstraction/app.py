from flask import Flask, render_template, request, redirect, url_for

import database

# remember to $ pip install flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
@app.route("/pets",methods=["GET"])
def get_pets():
    pet_data = database.retrieve_pets()
    return render_template("pets.html", data=pet_data)

@app.route("/create", methods=["GET"])
def get_create():
    return render_template("create.html")

@app.route("/create", methods=["POST"])
def post_create():
    name = request.form.get("name")
    kind = request.form.get("kind")
    noise = request.form.get("noise")
    food = request.form.get("food")
    pet_item = {
        "name":name,
        "kind":kind,
        "noise":noise,
        "food":food
    }
    database.create_pet(pet_item)
    return redirect(url_for("get_pets"))

@app.route("/edit/<id>", methods=["GET"])
def get_edit(id):
    pet = database.retrieve_pet(id)
    return render_template("edit.html", pet=pet)

@app.route("/edit/<id>", methods=["POST"])
def post_edit(id):
    name = request.form.get("name")
    kind = request.form.get("kind")
    noise = request.form.get("noise")
    food = request.form.get("food")
    pet_item = {
        "id":id,
        "name":name,
        "kind":kind,
        "noise":noise,
        "food":food
    }
    database.update_pet(pet_item)
    return redirect(url_for("get_pets"))

@app.route("/delete/<id>", methods=["GET"])
def get_delete(id): 
    database.delete_pet(id)
    return redirect(url_for("get_pets"))

