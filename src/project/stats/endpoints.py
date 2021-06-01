from flask import Blueprint, request, jsonify
from .service import StatsService

stats_blueprint = Blueprint('stats', __name__)


@stats_blueprint.route('/activity/<string:email>', methods=['GET'])
def activity(email) -> dict:
    events = StatsService.get_activity_by_email(
        email=email
    )
    return jsonify(events), 200
