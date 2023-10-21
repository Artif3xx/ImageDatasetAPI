"""
Main file of the fastapi. All the structured things are located here.
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.src.endpoints import upload, image, info, item, search
from api.src.database import models
from api.src.database.database import engine

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


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    """
    get the main index page of the project

    :return: the index template as response
    """
    return templates.TemplateResponse("index.html", {"request": request})
