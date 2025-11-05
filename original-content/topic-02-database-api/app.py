from flask import Flask, render_template, request, redirect, url_for

import sqlite3

# remember to $ pip install flask

app = Flask(__name__)

connection = sqlite3.connect("pets.db", check_same_thread=False)

@app.route("/", methods=["GET"])
@app.route("/pets",methods=["GET"])
def get_pets():
    cursor = connection.cursor()
    rows = cursor.execute("select * from pet").fetchall()
    pet_data = [
        {
            "id":str(id),
            "name":name,
            "kind":kind,
            "noise":noise,
            "food":food
        }
        for id, name, kind, noise, food in rows
    ]
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

    cursor = connection.cursor()
    cursor.execute("insert into pet (name, kind, noise, food) values (?, ?, ?, ?)", (name, kind, noise, food))
    connection.commit()

    return redirect(url_for("get_pets"))

@app.route("/edit/<id>", methods=["GET"])
def get_edit(id):
    cursor = connection.cursor()
    row = cursor.execute("select * from pet where id = ?", (id,)).fetchone()
    pet = {
        "id":str(row[0]),
        "name":row[1],
        "kind":row[2],
        "noise":row[3],
        "food":row[4]
    }
    return render_template("edit.html", pet=pet)

@app.route("/edit/<id>", methods=["POST"])
def post_edit(id):
    name = request.form.get("name")
    kind = request.form.get("kind")
    noise = request.form.get("noise")
    food = request.form.get("food")

    cursor = connection.cursor()
    cursor.execute("update pet set name = ?, kind = ?, noise = ?, food = ? where id = ?", (name, kind, noise, food, id))
    connection.commit()

    return redirect(url_for("get_pets"))

@app.route("/delete/<id>", methods=["GET"])
def get_delete(id): 
    cursor = connection.cursor()
    cursor.execute("delete from pet where id = ?", (id,))
    connection.commit()
    return redirect(url_for("get_pets"))

@app.route("/data", methods=["GET"])
def get_data():
    return {"data":[{
        "name":"Greg",
        "title":"Dr."

    },
    {
        "name":"Maletic",
        "title":"Professort."

    }
    ]}
