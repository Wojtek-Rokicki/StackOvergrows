import selenium
from selenium.webdriver.common.by import By

def get_cookie_accept_button(driver: selenium.webdriver.chrome.webdriver.WebDriver, 
                             cookie_button_access_type: str, cookie_button_access_id: str):
    accept_button = None
    if cookie_button_access_type == 'class':
        accept_button =  driver.find_element(By.CLASS_NAME, cookie_button_access_id)
    elif cookie_button_access_type == 'id':
        accept_button =  driver.find_element(By.ID, cookie_button_access_id)
    elif cookie_button_access_type == 'innerText':
        accept_button =  driver.find_element(By.XPATH, f"//*[text()='{cookie_button_access_id}']")
    return accept_button
    
def get_ad_elements(driver: selenium.webdriver.chrome.webdriver.WebDriver, 
                             ad_element_access_type: str, ad_element_access_id: str):
    ad_elements = None
    if ad_element_access_type == 'class':
        ad_elements = driver.find_elements(By.CLASS_NAME, ad_element_access_id)
    elif ad_element_access_type == 'classes':
        common = None
        for x in ad_element_access_id.split():
            elements = driver.find_elements(By.CLASS_NAME, x)
            if common is None:
                common = set(elements)
                continue
            else:
                common = common.intersection(set(elements))
        ad_elements = list(common)

    return ad_elements

def get_google_ads(driver: selenium.webdriver.chrome.webdriver.WebDriver):
    ad_elements = None
    try:
        ad_elements = driver.find_elements(By.XPATH, "//*[@aria-label='Advertisement']")
    except Exception:
        print("[Error] no elements were found.")
    return ad_elements

