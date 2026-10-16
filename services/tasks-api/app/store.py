class TaskStore:
    """In-memory task storage. Swapped for a real backend later."""

    def __init__(self):
        self._tasks = {}
        self._next_id = 1

    def add(self, title: str, normalized: bool) -> dict:
        task = {"id": self._next_id, "title": title, "normalized": normalized}
        self._tasks[task["id"]] = task
        self._next_id += 1
        return task

    def list(self) -> list:
        return list(self._tasks.values())

    def get(self, task_id: int):
        return self._tasks.get(task_id)

    def delete(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None
