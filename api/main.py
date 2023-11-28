"""
Main file of the fastapi. All the structured things are located here.
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

from api.src.endpoints import upload, image, info, item, search
from api.src.database import models
from api.src.database.database import engine

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="api/templates")

package_info = json.load(open("api/package.json"))

# create a fastapi instance
app = FastAPI(
    title=package_info["name"],
    version=package_info["version"],
    description=package_info["description"],

    # some extra settings for the swagger ui
    docs_url="/docs/swagger-ui",
    openapi_url="/docs/openapi.json",
    redoc_url=None,
    swagger_ui_parameters={
        'filter': False,
        'docExpansion': "list",
    },
    openapi_tags=[
        {"name": "Upload Routes",
         "description": "Routes for uploading images to the server"},
        {"name": "Image Routes",
         "description": "Routes for getting images from the server"},
        {"name": "Info Routes",
         "description": "Routes for getting information about the server"},
        {"name": "Item Routes",
         "description": "Routes for getting information about items"},
        {"name": "Search Routes",
         "description": "Routes for searching items"},
        {"name": "HTML pages",
         "description": "HTML pages of the project"}
    ],
    license_info={
        "name": "Apache 2.0 License",
        "identifier": "MIT",
    }
)

# mount the static folder to the api
app.mount("/static", StaticFiles(directory="api/static/"), name="static")

# include route inside the endpoints folder
app.include_router(upload.router)
app.include_router(image.router)
app.include_router(info.router)
app.include_router(item.router)
app.include_router(search.router)


@app.get("/", response_class=HTMLResponse, tags=["HTML pages"])
async def get_index(request: Request):
    """
    Get the main index page of the project \f

    :return: the index template as response
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/docs", response_class=HTMLResponse, tags=["HTML pages"])
async def get_docsWrap(request: Request):
    """
    Get the docs html page of the project \f

    :param request: the web request
    :return: the docs template as response
    """
    return templates.TemplateResponse("docs.html", {"request": request})


@app.get("/imageview", response_class=HTMLResponse, tags=["HTML pages"])
async def get_imageView(request: Request):
    """
    Get the image view page of the project \f

    :param request: web request
    :return: the image view template as response
    """
    return templates.TemplateResponse("imageview.html", {"request": request})


@app.get("/upload", response_class=HTMLResponse, tags=["HTML pages"])
async def get_upload(request: Request):
    """
    Get the upload page of the project \f

    :param request: web request
    :return: the upload template as response
    """
    return templates.TemplateResponse("upload.html", {"request": request})
