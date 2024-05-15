from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@localhost/test"
db = SQLAlchemy(app)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), nullable= False)
    amount = db.Column(db.Float, nullable=False)

@app.route("/incomes", methods=["POST"])
def create_income():
    data = request.json
    income = Income(amount=data["amount"], name=data["name"])
    db.session.add(income)
    db.session.commit()
    return jsonify({"id": income.id}), 201

@app.route("/incomes/<int:id>", methods=["GET"])
def get_income_by_id(id):
    income = Income.query.get(id)
    if income is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"id": income.id, "name": income.name, "amount": income.amount })

@app.route("/incomes", methods=["GET"])
def get_all_incomes():
    incomes = Income.query.all()
    with open("incomes.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id","name","amount"])
        for income in incomes:
            writer.writerow([income.id, income.name, income.amount])
            
    return jsonify({"message": "CSV file generated successfully"}), 200

@app.route("/incomes/<int:id>", methods=["PUT"])
def update_income(id):
    income = Income.query.get(id)
    if income is None:
        return jsonify({"error": "Not found"}), 404
    data = request.json
    income.name = data["name"]
    income.amount = data["amount"]
    db.session.commit()
    return jsonify({"id": income.id, "name": income.name, "amount": income.amount})

@app.route("/incomes/<int:id>", methods=["DELETE"])
def delete_income(id):
    income = Income.query.get(id)
    if income is None:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(income)
    db.session.commit()
    return jsonify({"message": "Income deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
