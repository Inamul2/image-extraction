from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import os

class Youtube_Scrapper:

    def decision(self, url):
        try:

            links = self.youtube_com(url)

            response = {"Success": True, "Data Scraped": links, "Status Code": 200}

        except Exception as e:

            response = {"Success": False, "Message": "Some Internal Issue has been occured - " + str(e), "Status Code": 500}

        return response

    def getFavicon(self, domain):
        favicons = []
        page = requests.get(domain)
        soup = BeautifulSoup(page.text, 'html.parser')
        icon_link = soup.find_all("link", rel="shortcut icon")
        if icon_link is None:
            icon_link = soup.find_all("link", rel="icon")
        if icon_link is None:
            return [domain + '/favicon.ico']
        else:
            for fav in icon_link:
                favicons.append(fav["href"])
        return favicons

    def youtube_com(self, baseUrl):
        images_src_json = []
        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1420,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
        try:
            driver.implicitly_wait(5)
            collection_of_images = []
            driver.get(baseUrl)
            time.sleep(5)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            time.sleep(5)
            total_elements = driver.find_elements(By.XPATH, '//*[@id="img"]')
            for check_elem in total_elements:
                get_elem = str(check_elem.get_attribute("src"))
                if ".com" in get_elem:
                    collection_of_images.append(get_elem)

            final_file = collection_of_images
            favicon_data = self.getFavicon(baseUrl)
            time.sleep(5)
            for check in range(len(final_file)):
                alpha = {
                    "URL": final_file[check]
                }
                images_src_json.append(alpha)
            for fav in favicon_data:
                favor = {
                    "Favicon": fav
                }
                images_src_json.append(favor)

        finally:
            driver.quit()

        return images_src_json
