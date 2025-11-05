from flask import Flask, render_template, request, redirect, url_for

import database

# remember to $ pip install flask

database.initialize("pets.db")

app = Flask(__name__)

@app.route("/", methods=["GET"]) 
@app.route("/list", methods=["GET"])
def get_list():
    pets = database.get_pets()
    return render_template("list.html", pets=pets)     


@app.route("/kind", methods=["GET"])
@app.route("/kind/list", methods=["GET"])
def get_kind_list():
    kinds = database.get_kinds()
    return render_template("kind_list.html", kinds=kinds)


@app.route("/create", methods=["GET"])
def get_create():
    kinds = database.get_kinds()
    print("KINDS = ",kinds)
    return render_template("create.html", kinds=kinds)     

@app.route("/create", methods=["POST"])
def post_create():
    data = dict(request.form)
    print("DATA=",data)
    database.create_pet(data)
    return redirect(url_for("get_list"))  

@app.route("/delete/<id>", methods=["GET"])
def get_delete(id):
    database.delete_pet(id)
    return redirect(url_for("get_list"))  

@app.route("/update/<id>", methods=["GET"])
def get_update(id):
    data = database.get_pet(id)
    return render_template("update.html",data=data)

@app.route("/update/<id>", methods=["POST"])
def post_update(id):
    data = dict(request.form)
    database.update_pet(id, data)
    return redirect(url_for("get_list"))  

@app.route("/kind/create", methods=["GET"])
def get_kind_create():
        return render_template("kind_create.html")

@app.route("/kind/create", methods=["POST"])
def post_kind_create():
    data = dict(request.form)
    database.create_kind(data)
    return redirect(url_for("get_kind_list"))

@app.route("/kind/delete/<id>", methods=["GET"])
def get_kind_delete(id):
    try:
        database.delete_kind(id)
    except Exception as e:
        return render_template("error.html", error_text=str(e))
    return redirect(url_for("get_kind_list"))

@app.route("/kind/update/<id>", methods=["GET"])
def get_kind_update(id):
    data = database.get_kind(id)
    return render_template("kind_update.html",data=data)

@app.route("/kind/update/<id>", methods=["POST"])
def post_kind_update(id):
    data = dict(request.form)
    database.update_kind(id, data)
    return redirect(url_for("get_kind_list"))
