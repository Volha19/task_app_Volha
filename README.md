# Tasks app: two small services

A to-do API that calls a tiny stateless function to clean up task titles.

| Service | Folder | Port | What it does |
|---|---|---|---|
| tasks-api | `services/tasks-api` | 5000 | CRUD for tasks. Calls `title-normalizer` when a task is created. |
| title-normalizer | `services/title-normalizer` | 5001 | One function: `POST /invoke` trims a title, collapses spaces, capitalizes the first letter. |

If `title-normalizer` is down, `tasks-api` still creates the task with the raw title and `"normalized": false`.

## Endpoints

tasks-api:

- `GET /health`
- `GET /tasks`
- `POST /tasks` with `{"title": "..."}`: 201, or 400 for an empty title or a non-JSON body
- `GET /tasks/<id>`: 200 or 404
- `DELETE /tasks/<id>`: 204 or 404

title-normalizer:

- `GET /health`
- `POST /invoke` with `{"title": "  buy   milk "}` returns `{"title": "Buy milk"}`; 400 if `title` is not a string

## Run (two terminals)

Each service has its own `requirements.txt`.

```bash
# terminal 1
cd services/title-normalizer
pip install -r requirements.txt
flask --app app:create_app run --port 5001

# terminal 2
cd services/tasks-api
pip install -r requirements.txt
NORMALIZER_URL=http://localhost:5001 flask --app app:create_app run --port 5000
```

Try it:

```bash
curl -X POST localhost:5000/tasks -H 'Content-Type: application/json' -d '{"title": "  buy   milk "}'
curl localhost:5000/tasks
```

Stop terminal 1 and create another task: it still works, with `"normalized": false`.

## Test

Run in each service folder:

```bash
pytest
```

## Publish container images

Pushing to `main` runs `.github/workflows/publish-images.yml`, which builds and
publishes both service images to GitHub Container Registry:

- `ghcr.io/<owner>/<repository>-tasks-api`
- `ghcr.io/<owner>/<repository>-title-normalizer`

The workflow uses the automatic `GITHUB_TOKEN`; its publish job grants only
`contents: read` and `packages: write`. The repository's Actions settings must
allow workflows to write packages.
