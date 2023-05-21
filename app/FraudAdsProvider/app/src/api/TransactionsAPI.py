from typing import List
from pydantic import ValidationError

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json

import requests


from app.src.api.models import (InputDataSite,
                                InputDataBrowser,
                                ResponseData)


class TransactionsAPI:
    ADS_SCRAPPER_ADDRESS = "192.168.100.94:8002"
    ADS_SCRAPPER_SHARED_DIR_ADDRESS = "192.168.100.94:9000/AdsScrapper"

    def __init__(self):
        self.module = None

    async def get_ads_browser(self, input: InputDataBrowser) -> List:
        """
        Call module Ads Scrapper
        """
        return await self.call_get_request_browser(input)

    async def get_ads_site(self, input: InputDataSite) -> List:
        """
        Call module Ads Scrapper
        """
        return await self.call_get_request_site(input)

    async def call_get_request_browser(self, input: InputDataBrowser):
        url = f'http://{self.ADS_SCRAPPER_ADDRESS}/get_ads_browser'

        response = requests.post(
            url=url,
            data=input.json()
        )
        if not response.ok:
            return Response(
                status_code=response.status_code
            )
        return JSONResponse(response.json())

    async def call_get_request_site(self, input: InputDataSite):
        url = f'http://{self.ADS_SCRAPPER_ADDRESS}/get_ads_site'

        response = requests.post(
            url=url,
            data=input.json()
        )
        if not response.ok:
            return Response(
                status_code=response.status_code
            )
        return JSONResponse(response.json())

    async def get_response_query_site(self, input: InputDataSite):
        #
        # Handler for receiving final ads list
        #
        response = await self.get_ads_site(input)
        response = response.body.decode()
        response = json.loads(response)
        if response:
            return self.get_modified_screenshots_path(response)
        else:
            return {"ads": "no ads detected"}

    def get_modified_screenshots_path(self, response):

        response["screenshot_ads"] = [f"{self.ADS_SCRAPPER_SHARED_DIR_ADDRESS}{link}" for link in response["screenshot_ads"]]
        return response

    async def get_response_query_browser(self, input: InputDataBrowser):
        response = await self.get_ads_browser(input)
        response = response.body.decode()
        response = json.loads(response)
        print(response)
        if response:
            return self.get_modified_screenshots_path(response)
        else:
            return {"ads": "no ads detected"}
        return response
