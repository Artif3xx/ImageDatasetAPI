from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from api.endpoints import upload, image, labels, info
from api.database.database import Database

# init the database with the path to the database file
Database('data/Database.db')
templates = Jinja2Templates(directory="api/templates")
# create a fastapi instance
app = FastAPI()
# mount the static folder to the api
app.mount("/static", StaticFiles(directory="api/static/"), name="static")
# include route inside the endpoints folder
app.include_router(upload.router)
app.include_router(image.router)
app.include_router(labels.router)
app.include_router(info.router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Redirects to the docs page

    :return: a redirect to the docs page
    """
    return templates.TemplateResponse("index.html", {"request": request})
