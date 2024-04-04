import uvicorn
from fastapi import FastAPI

from v1.routers import all_routers


def create_app() -> FastAPI:
    app = FastAPI(title="Соц сеть")

    for router in all_routers:
        app.include_router(router)

    return app


app = create_app()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
