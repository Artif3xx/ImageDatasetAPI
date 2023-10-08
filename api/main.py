from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse

from api.endpoints import upload, random, labels, info
from api.database.database import Database

# init the database with the path to the database file
Database('data/Database.db')

app = FastAPI()

# include route inside the endpoints folder
app.include_router(upload.router)
app.include_router(random.router)
app.include_router(labels.router)
app.include_router(info.router)


@app.get("/")
async def root():
    """
    Redirects to the docs page

    :return: a redirect to the docs page
    """
    return RedirectResponse(url='/docs')
