from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from api.src.endpoints import upload, image, info, item, search

from sqlalchemy.orm import Session

from api.src.database import crud, models, schemas
from api.src.database.database import get_db, engine

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="api/templates")

# create a fastapi instance
app = FastAPI()
# mount the static folder to the api

# include route inside the endpoints folder
app.include_router(upload.router)
app.include_router(image.router)
app.include_router(info.router)
app.include_router(item.router)
app.include_router(search.router)


@app.get("/")
async def root():
    """
    Redirects to the docs page

    :return: a redirect to the docs page
    """
    return FileResponse("api/static/html/index.html")

