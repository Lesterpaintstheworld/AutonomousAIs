from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/musicpatterns")
mongo = PyMongo(app)

@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Community Music Pattern Creator API"})

@app.route("/patterns", methods=["GET"])
def get_patterns():
    patterns = list(mongo.db.patterns.find())
    return jsonify([{**pattern, "_id": str(pattern["_id"])} for pattern in patterns])

@app.route("/patterns", methods=["POST"])
def create_pattern():
    new_pattern = request.json
    result = mongo.db.patterns.insert_one(new_pattern)
    return jsonify({"id": str(result.inserted_id)}), 201

@app.route("/patterns/<id>", methods=["GET"])
def get_pattern(id):
    pattern = mongo.db.patterns.find_one({"_id": ObjectId(id)})
    if pattern:
        pattern["_id"] = str(pattern["_id"])
        return jsonify(pattern)
    return jsonify({"error": "Pattern not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
