from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import csv

URLs = ["https://www.google.com/search?q=baltic+pipe", \
        "https://www.google.com/search?q=inwestowanie+w+akcje"]

for id, url in enumerate(URLs):

    driver = webdriver.Chrome("chromedriver_mac_arm64/chromedriver")

    driver.get(url)

    max_wait_time = 10
    WebDriverWait(driver, max_wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    element =   driver.find_element(By.XPATH, "//*[text()='Accept all']") # Dla [pl] Zaakceptuj wszystko
   
    if element is not None:
        element.click()
    else:
        print("Button was not found")

    attribute_name = "data-text-ad"
    elements = driver.find_elements(By.CSS_SELECTOR, f"[{attribute_name}]")

    header = ['title', 'url', 'description']

    with open(str(id)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for element in elements:
            # e = element.find_element(By.XPATH, ".//div[@role='heading']")
            # print(e.text)
            element_text = element.text.split('\n')
            data = [element_text[1], element_text[3], ''.join(element_text[4:])]
            writer.writerow(data)

            # https://www.w3schools.com/xml/xpath_syntax.asp


    driver.save_screenshot(str(id)+".png")