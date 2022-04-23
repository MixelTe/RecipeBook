from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
import logging


blueprint = Blueprint(
    'other',
    __name__,
    template_folder='templates'
)
logger = logging.getLogger("other")


def time():
    utc_dt = datetime.utcnow()
    utc_dt += timedelta(hours=3)
    return utc_dt


@blueprint.route("/other/tlop/access/<int:code>")
def tlop_access(code):
    logger.info(f"{request.remote_addr} - Code: {code} Access: {'true' if code == 0 else 'false'}")
    return jsonify({"access": code == 0}), 200
