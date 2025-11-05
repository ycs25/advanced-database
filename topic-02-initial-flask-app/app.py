from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# remember to $ pip install flask


connection = sqlite3.connect("pets.db", check_same_thread=False)

app = Flask(__name__)

@app.route("/", methods=["GET"]) 
def get_index():
    return("Example flask server.")

@app.route("/hello", methods=["GET"]) 
@app.route("/hello/<name>", methods=["GET"]) 
def get_hello(name="world"):
    data = [
        {"name":"bob","age":10},
        {"name":"suzy","age":8},
    ]
    return render_template("hello.html", data=data, prof={"name":name, "title":"Dr."})

@app.route("/bye", methods=["GET"])
def get_bye():
    return("Well, goodbye, then!")

@app.route("/list", methods=["GET"])
def get_list():
    cursor = connection.cursor()
    cursor.execute("""select * from pets""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return render_template("list.html", rows=rows)     

@app.route("/create", methods=["GET"])
def get_create():
    return render_template("create.html")     

@app.route("/create", methods=["POST"])
def post_create():
    data = dict(request.form)
    try:
        data["age"] = int(data["age"])
    except: 
        data["age"] = 0
    print(data)
    cursor = connection.cursor()
    cursor.execute("""insert into pets(name, age, type, owner) values (?,?,?,?)""",
        (data["name"],data["age"],data["type"],data["owner"]))
    rows = cursor.fetchall()
    connection.commit()
    return redirect(url_for("get_list"))  

@app.route("/delete/<id>", methods=["GET"])
def get_delete(id):
    cursor = connection.cursor()
    cursor.execute(f"""delete from pets where id = ?""",(id,))
    connection.commit()
    return redirect(url_for("get_list"))  

@app.route("/update/<id>", methods=["GET"])
def get_update(id):
    cursor = connection.cursor()
    cursor.execute(f"""select * from pets where id = ?""",(id,))
    rows = cursor.fetchall()
    try:
        (id, name, xtype, age, owner) = rows[0]
        data = {
                "id":id,
                "name":name,
                "type":xtype,
                "age":age,
                "owner":owner
        }
        print([data])
    except:
        return "Data not found."
    return render_template("update.html",data=data)

@app.route("/update/<id>", methods=["POST"])
def post_update(id):
    data = dict(request.form)
    try:
        data["age"] = int(data["age"])
    except: 
        data["age"] = 0
    print(data)
    cursor = connection.cursor()
    cursor.execute("""update pets set name=?, age=?, type=?, owner=? where id=?""",
        (data["name"],data["age"],data["type"],data["owner"],id))
    rows = cursor.fetchall()
    connection.commit()
    return redirect(url_for("get_list"))  
