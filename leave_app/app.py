# imports
from flask import Flask, render_template, request
from flask import redirect
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["leave_db"]
collection = db["leave_requests"]

# Home page
@app.route("/")
def home():
    return render_template("apply.html")

# Apply leave
@app.route("/apply", methods=["POST"])
def apply():
    emp_id = request.form["emp_id"]
    from_date = request.form["from_date"]
    to_date = request.form["to_date"]
    reason = request.form["reason"]

    data = {
        "emp_id": emp_id,
        "from_date": from_date,
        "to_date": to_date,
        "reason": reason,
        "status": "Pending",
        "applied_on": datetime.now()
    }

    collection.insert_one(data)

    return "Leave Applied Successfully!"

@app.route("/status", methods=["GET", "POST"])
def status():
    if request.method == "POST":
        emp_id = request.form["emp_id"]
        leaves = list(collection.find({"emp_id": emp_id}))
        return render_template("status.html", leaves=leaves)
    
    return render_template("status.html")
@app.route("/admin")
def admin():
    leaves = list(collection.find())
    return render_template("admin.html", leaves=leaves)
@app.route("/approve/<id>")
def approve(id):
    collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "Approved"}}
    )
    return redirect("/admin")
@app.route("/reject/<id>")
def reject(id):
    collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "Rejected"}}
    )
    return redirect("/admin")

# run app
if __name__ == "__main__":
    app.run(debug=True)