from flask import Blueprint, jsonify, request

bp = Blueprint("normalizer", __name__)


def normalize(title: str) -> str:
    """Trim, collapse whitespace, uppercase the first letter. Rest is untouched."""
    cleaned = " ".join(title.split())
    return cleaned[:1].upper() + cleaned[1:]


@bp.get("/health")
def health():
    return jsonify(status="ok")


@bp.post("/invoke")
def invoke():
    data = request.get_json(silent=True)
    title = data.get("title") if isinstance(data, dict) else None
    if not isinstance(title, str):
        return jsonify(error="title must be a string"), 400
    return jsonify(title=normalize(title))
