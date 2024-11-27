from flask import Flask, request, jsonify, abort
from functools import wraps
from dotenv import load_dotenv
import os
import hmac

load_dotenv()

API_KEY = os.getenv('API_KEY')

app = Flask(__name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')

        if not auth or not auth.startswith("Bearer "):
            abort(401, description="Unauthorized: Missing or invalid token")

        token = auth.split(" ")[1]

        if not hmac.compare_digest(token, API_KEY):
            abort(401, description="Unauthorized: Invalid token")

        return f(*args, **kwargs)
    return decorated


@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({"error": error.description}), 401


@app.route('/')
@token_required
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
