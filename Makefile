lint:
	black .
	ruff check . --fix

dev:
	cd src && uvicorn main:app --reload

runprod:
	alembic upgrade head
	cd src && uvicorn main:app --reload --host 0.0.0.0
