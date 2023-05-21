from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.src.api.TransactionsAPI import TransactionsAPI
from app.src.api.models import (InputDataSite,
                                InputDataBrowser)


app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)


### MOUNT IMAGE LOCAL FOLDER ###
app.mount("/AdsScrapper/ads_images", StaticFiles(directory="/ads_images"), name="imgs")

### ENDPOINTS ###

transactions_api = TransactionsAPI()


@app.post("/query_site")
async def query_site(input: InputDataSite):
    return await transactions_api.get_response_query_site(input)


@app.post("/query_browser")
async def query_site(input: InputDataBrowser):
    return await transactions_api.get_response_query_browser(input)
