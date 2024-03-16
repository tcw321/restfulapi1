#Generated from AI Claude 3 Opus March 16, 2024
from flask import Flask, request, jsonify
import jwt
import os

app = Flask(__name__)

# Get the secret key from the environment variable
SECRET_KEY = os.environ.get("SECRET_KEY")

# Get the username and password from the environment variables
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

# Dummy user credentials (replace with actual user database)
USER_CREDENTIALS = {
    ADMIN_USERNAME: ADMIN_PASSWORD
}

# Route for login
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Route for multiplying a number
@app.route("/multiply", methods=["POST"])
def multiply():
    token = request.headers.get("Authorization").split(" ")[1]
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        number = request.json.get("number")
        result = number * 2
        return jsonify({"result": result})
    except jwt.DecodeError:
        return jsonify({"message": "Invalid token"}), 401

if __name__ == "__main__":
    app.run()