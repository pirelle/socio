lint:
	black .
	ruff check . --fix

dev:
	cd src && uvicorn main:app --reload
