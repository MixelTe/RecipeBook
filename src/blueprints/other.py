from datetime import datetime, timedelta
from flask import Blueprint, jsonify


blueprint = Blueprint(
    'other',
    __name__,
    template_folder='templates'
)


def time():
    utc_dt = datetime.utcnow()
    utc_dt += timedelta(hours=3)
    return utc_dt


@blueprint.route("/other/tlop/access/<int:code>")
def tlop_access(code):
    return jsonify({"access": code == 0}), 200
