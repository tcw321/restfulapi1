#Generated from AI Claude 3 Opus March 16, 2024
from flask import Flask, request, jsonify
import jwt
import os
from datetime import datetime, timedelta

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

valid_tokens = {}

# Route for login
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        token = jwt.encode({"username": username, "exp": datetime.utcnow() + timedelta(minutes=30)}, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Route for multiplying a number
@app.route("/multiply", methods=["POST"])
def multiply():
    token = request.headers.get("Authorization").split(" ")[1]
    if token in valid_tokens:
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            number = request.json.get("number")
            result = number * 2
            return jsonify({"result": result})
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
    else:
        return jsonify({"message": "Invalid token"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization").split(" ")[1]
    if token in valid_tokens:
        del valid_tokens[token]
        return jsonify({"message": "Logged out successfully"})
    else:
        return jsonify({"message": "Invalid token"}), 401

if __name__ == "__main__":
    app.run()