import logging
import os
import werkzeug
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.middleware.profiler import ProfilerMiddleware


db = SQLAlchemy()
migrate = Migrate()


def register_blueprints(app: Flask) -> None:
    from project.heartbeat.endpoints import heartbeat_blueprint
    from project.sendgrid.endpoints import sendgrid_blueprint
    from project.stats.endpoints import stats_blueprint
    app.register_blueprint(heartbeat_blueprint)
    app.register_blueprint(sendgrid_blueprint)
    app.register_blueprint(stats_blueprint)
    

def register_error_handlers(app: Flask) -> None:
    def handle_validation_error(e):
        return jsonify(e.messages), 400

    @app.errorhandler(werkzeug.exceptions.BadRequest)
    @app.errorhandler(werkzeug.exceptions.Unauthorized)
    @app.errorhandler(werkzeug.exceptions.Forbidden)
    @app.errorhandler(werkzeug.exceptions.NotFound)
    @app.errorhandler(werkzeug.exceptions.InternalServerError)
    @app.errorhandler(Exception)
    def json_error_handler(e: Exception) -> tuple:
        if isinstance(e, werkzeug.exceptions.HTTPException):
            return jsonify(error=e.code, description=e.description), e.code
        return jsonify(error=500, description=str(e)), 500


def is_profiling() -> bool:
    profiling = os.getenv('PROFILING')
    return profiling is not None and profiling == '1'


def create_app(script_info: str = None) -> Flask:
    app = Flask(__name__)

    CORS(app)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)

    migrate.init_app(app, db)

    register_blueprints(app)
    if os.getenv('FLASK_ENV') == 'production':
        register_error_handlers(app)

    if is_profiling():
        app.wsgi_app = ProfilerMiddleware(
            app.wsgi_app,
            sort_by=('cumtime', 'ncalls'))

    @app.shell_context_processor
    def ctx() -> dict:
        return {'app': app, 'db': db}

    return app


logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

import logging
es_trace_logger = logging.getLogger('elasticsearch.trace')
es_trace_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
es_trace_logger.addHandler(handler)