import os

from flask import Flask

from app.normalizer import NormalizerClient
from app.routes import bp
from app.store import TaskStore


def create_app(store=None, normalizer=None) -> Flask:
    app = Flask(__name__)
    app.config["STORE"] = store if store is not None else TaskStore()
    app.config["NORMALIZER"] = (
        normalizer
        if normalizer is not None
        else NormalizerClient(os.environ.get("NORMALIZER_URL", "http://localhost:5001"))
    )
    app.register_blueprint(bp)
    return app
