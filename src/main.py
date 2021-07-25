from fastapi import FastAPI
from starlette.responses import RedirectResponse
import uvicorn
from routers import weather

app = FastAPI()


@app.get("/", response_class=RedirectResponse)
async def root() -> RedirectResponse:
    return RedirectResponse("/docs")


def configure_router():
    app.include_router(weather.router)


def configure():
    configure_router()


if __name__ == "__main__":
    configure()
    uvicorn.run(app, port=8080, host="localhost")
else:
    configure()
