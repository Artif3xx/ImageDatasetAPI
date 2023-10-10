from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.endpoints import upload, image, labels, info
from api.database.database import Database

# init the database with the path to the database file
Database('data/Database.db')

# create a fastapi instance
app = FastAPI()
# mount the static folder to the api

# include route inside the endpoints folder
app.include_router(upload.router)
app.include_router(image.router)
app.include_router(labels.router)
app.include_router(info.router)


@app.get("/")
async def root():
    """
    Redirects to the docs page

    :return: a redirect to the docs page
    """
    return FileResponse("api/static/html/index.html")
