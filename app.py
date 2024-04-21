from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime


app = Flask(__name__)

# MongoDB Atlas connection
app.config["MONGO_URI"] = "mongodb+srv://yuhao:zyh123456@cluster0.6xunfrl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

# Select the database
db = mongo.db

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/read')
def read():
    designs = db.exampleapp.find()
    return render_template("read.html", designs=designs) 

@app.route('/create', methods=["GET"])
def create(): 
    return render_template("create.html") 

@app.route("/create", methods=["POST"])
def create_post():
    document = {
        "name": request.form["customer_name"],
        "coffee_beans": request.form["coffee_beans"],
        "shots": request.form["shots"],
        "cup_size": request.form["cup_size"],
        "created_at": datetime.utcnow()
    }
    db.exampleapp.insert_one(document)
    return redirect(url_for("read"))

@app.route("/edit/<mongoid>", methods=["GET", "POST"])
def edit_post(mongoid):
    if request.method == "POST":
        updated_doc = {
            "name": request.form["customer_name"],
            "coffee_beans": request.form["coffee_beans"],
            "shots": request.form["shots"],
            "cup_size": request.form["cup_size"],
            "updated_at": datetime.utcnow()
        }
        db.exampleapp.update_one({"_id": ObjectId(mongoid)}, {"$set": updated_doc})
        return redirect(url_for("read"))
    else:
        design = db.exampleapp.find_one({"_id": ObjectId(mongoid)})
        return render_template("edit.html", design=design)

@app.route("/delete/<mongoid>")
def delete(mongoid):
    db.exampleapp.delete_one({"_id": ObjectId(mongoid)})
    return redirect(url_for("read"))

@app.errorhandler(Exception)
def handle_error(e):
    return render_template("error.html", error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)