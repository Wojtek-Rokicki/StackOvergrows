from fastapi import FastAPI

from app.models import InputDataBrowser
from app.utils import get_cookie_accept_button, get_ad_elements
from fastapi.middleware.cors import CORSMiddleware
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import shutil
import time

from urllib.parse import urlparse




AVAILABLE_SERVICES = {
    'interia': {
        'cookie_button_access_type': 'class',
        'cookie_button_access_id': 'rodo-popup-agree',
        'ad_element_access_type': 'class',
        'ad_element_access_id': 'ad-container-loaded'},

    'onet': {
        'cookie_button_access_type': 'class',
        'cookie_button_access_id': 'cmp-intro_acceptAll',
        'ad_element_access_type': 'class',
        'ad_element_access_id': 'ad_wrapper'},

    'wykop': {
        'cookie_button_access_type': 'innerText',
        'cookie_button_access_id': 'Accept All',
        'ad_element_access_type': 'classes',
        'ad_element_access_id': 'pub-slot-wrapper loaded'},
    'newsweek': {
        'cookie_button_access_type': 'class',
        'cookie_button_access_id': 'cmp-intro_acceptAll',
        'ad_element_access_type': 'class',
        'ad_element_access_id': 'ad_wrapper'
    },
    'biznes': {
        'cookie_button_access_type': 'class',
        'cookie_button_access_id': 'cmp-intro_acceptAll',
        'ad_element_access_type': 'class',
        'ad_element_access_id': 'ad_wrapper'
    }
}

# Global constants
WAIT_TIME = 5

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


def extract_entity_name(url):
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split('.')
    if domain_parts[0] == 'www':
        entity_name = domain_parts[1]
    else:
        entity_name = domain_parts[0]
    return entity_name

@app.post("/get_ads_site")
async def get_ads(input: dict):

    url = input['url']
    query = input['query']
    user_agent = input['user_agent']
    context = input['context']
    id_site = extract_entity_name(url)

    if id_site in AVAILABLE_SERVICES.keys():
        website = AVAILABLE_SERVICES[id_site]

        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')
        # options.add_argument("--headless")
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
        driver.get(url)

        # Wait for the webpage to load
        time.sleep(WAIT_TIME)

        accept_button = get_cookie_accept_button(driver, website['cookie_button_access_type'],
                                                 website['cookie_button_access_id'])
        if accept_button is not None:
            accept_button.click()
        else:
            print('[Error] Button was not found')
            exit(1)

        # Wait for the ads to load
        time.sleep(WAIT_TIME)

        ad_elements = get_ad_elements(driver, website['ad_element_access_type'], website['ad_element_access_id'])
        if ad_elements is None:
            print('[Error] Ads were not found')
            exit(1)

        path_dir = f"/ads_images/{id_site}"
        try:
            shutil.rmtree(path_dir)
        except FileNotFoundError:
            pass
        os.mkdir(path_dir)

        # Save main screenshot
        driver.save_screenshot(path_dir + '/main.png')

        # URLs for ads redirection
        redirect_links = []

        destinations_urls = []
        screenshots_urls = []

        # Save ads screenshots
        for id, ad_element in enumerate(ad_elements):
            first_href_element = ad_element.find_element(By.CSS_SELECTOR, "*[href]")
            print(first_href_element.get_attribute("href"))
            path_screen = path_dir + '/' + str(id) + '.png'
            print(f"Saving screen: {path_screen}")
            try:
                ad_element.screenshot(path_screen)
            except Exception:
                pass

            # Get final redirection link
            win_handle_before = driver.current_window_handle
            try:
                ad_element.click()
            except ElementClickInterceptedException:
                pass

            time.sleep(2)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(0.5)
            ad_url = driver.current_url
            driver.switch_to.window(win_handle_before)

            # Write ad's redirection link
            screenshots_urls.append(path_screen)
            destinations_urls.append(ad_url)

        return get_response(id_site, screenshots_urls, destinations_urls)
    else:
        pass


def get_response(id_site, screenshots_urls, destinations_urls, words=[]):
    response = {
        "name": id_site,
        "destination_url": destinations_urls,
        "words": words,
        "screenshot_ads": screenshots_urls
    }
    return response


def build_url_search(url, search: str):
    return f"{url}search?q={'+'.join(search.split())}"

@app.post("/get_ads_browser")
async def get_ads(input: dict):
    url = input['url']
    search = input['search']

    #query = input['query']
    user_agent = input['user_agent']
    #context = input['context']

    url_search = build_url_search(url, search)

    path_dir = f"/ads_images/{search}"

    for search_name, url in zip([search], [url_search]):
        print(search_name, url)

        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

        driver.get(url)

        max_wait_time = 10
        WebDriverWait(driver, max_wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # element = driver.find_element(By.XPATH, "//*[text()='Zaakceptuj wszystko']")  # Dla [pl] Zaakceptuj wszystko

        try:
            shutil.rmtree(path_dir)
        except FileNotFoundError:
            pass
        os.mkdir(path_dir)

        # if element is not None:
        #     element.click()
        # else:
        #     print("Button was not found")

        attribute_name = "data-text-ad"
        elements = driver.find_elements(By.CSS_SELECTOR, f"[{attribute_name}]")

        # Prepare data for each add
        names = []
        destination_urls = []
        words = []
        for element in elements:
            # e = element.find_element(By.XPATH, ".//div[@role='heading']")
            # print(e.text)
            element_text = element.text.split('\n')

            names.append(element_text[1])
            destination_urls.append(element_text[3])
            words.append(''.join(element_text[4:]))

        driver.save_screenshot(os.path.join(path_dir, str(search_name) + ".png"))
        screenshots_urls = [os.path.join(path_dir, str(search_name) + ".png")]

        print(names, screenshots_urls, destination_urls, words)
    return get_response(names, screenshots_urls, destination_urls, words)

