from flask import Blueprint, request
from .service import SendgridService

sendgrid_blueprint = Blueprint('sendgrid', __name__)


@sendgrid_blueprint.route('/sendgrid/hook', methods=['POST'])
def hook() -> dict:
    if not request.is_json:
        return({ 
            'err': True,
            'msg': 'No Body',
        }, 400)
        
    events = request.get_json(force=True, silent=True)
    print(events)
    if not isinstance(events, list):
        events = [events]
    for event in events:
        print('event', event)
        SendgridService.insert(event)
    return 'ok', 200
