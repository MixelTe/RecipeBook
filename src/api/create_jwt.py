from flask_jwt_simple.utils import _get_jwt_manager
from flask_jwt_simple.config import config
import jwt


def create_jwt(identity):
    jwt_manager = _get_jwt_manager()
    jwt_data = jwt_manager._get_jwt_data(identity)
    secret = config.encode_key
    algorithm = config.algorithm
    return jwt.encode(jwt_data, secret, algorithm)
