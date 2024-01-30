# Run the project:

## Docker
```bash
docker compose up --build
```

## Locally

```bash
poetry install
```
```bash
poetry shell
```
```bash
poetry run uvicorn main:app --host localhost --port 8001
```