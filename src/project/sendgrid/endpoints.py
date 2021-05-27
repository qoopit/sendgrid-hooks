from flask import Blueprint

sendgrid_blueprint = Blueprint('sendgrid', __name__)


@sendgrid_blueprint.route('/sendgrid/hook', methods=['GET'])
def hook() -> dict:
    return {
        'status': 'ok'
    }, 200
