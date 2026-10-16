from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("tasks", __name__)


@bp.get("/health")
def health():
    return jsonify(status="ok")


@bp.get("/tasks")
def list_tasks():
    return jsonify(current_app.config["STORE"].list())


@bp.post("/tasks")
def create_task():
    data = request.get_json(silent=True)
    title = data.get("title") if isinstance(data, dict) else None
    if not isinstance(title, str) or not title.strip():
        return jsonify(error="title is required"), 400

    normalized_title = current_app.config["NORMALIZER"].normalize(title)
    if normalized_title is None:
        task = current_app.config["STORE"].add(title, normalized=False)
    else:
        task = current_app.config["STORE"].add(normalized_title, normalized=True)
    return jsonify(task), 201


@bp.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = current_app.config["STORE"].get(task_id)
    if task is None:
        return jsonify(error="task not found"), 404
    return jsonify(task)


@bp.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    if not current_app.config["STORE"].delete(task_id):
        return jsonify(error="task not found"), 404
    return "", 204
