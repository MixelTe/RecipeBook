```py
from flask import Flask, jsonify, request
from flask_jwt_simple import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'secret_key'
jwt_manager = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    if (not request.is_json):
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    # check user data
    if (username != 'test' or password != 'test'):
        return jsonify({"msg": "Bad username or password"}), 401

    ret = {'jwt': create_jwt(identity=username)}
    return jsonify(ret), 200


# Protect a view with jwt_required, which requires a valid jwt
# to be present in the headers.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    return jsonify({'hello_from': get_jwt_identity()}), 200
```

## create_jwt
```py
from flask_jwt_simple.utils import _get_jwt_manager
from flask_jwt_simple.config import config
import jwt


def create_jwt(identity):
    jwt_manager = _get_jwt_manager()
    jwt_data = jwt_manager._get_jwt_data(identity)
    secret = config.encode_key
    algorithm = config.algorithm
    return jwt.encode(jwt_data, secret, algorithm)
```
