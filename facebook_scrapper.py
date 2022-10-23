from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import os
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import requests


class Facebook_scrapper:
    def decision(self, url):
        try:

            links = self.facebook_scraper(url)

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

    def fb_login(self,fb_paths, driver):
        """
        Facebook is hard to scrape, We have to use some advance techniques
        to scrape data - This function will help to login.
        """
        try:
            entry_input = driver.find_element_by_xpath(fb_paths[0])
        except:
            try:
                entry_input = driver.find_element_by_xpath(fb_paths[2])
            except:
                entry_input = driver.find_element_by_css_selector(fb_paths[1])

        return entry_input

    def facebook_scraper(self,check):
        """
        Facebook is one of the best secure websites in the world. We have to create
        an Advance function to scrape data from it - Complete Facebook Scraper
        """

        # Basic Requirements to run selenium within the function on HEROKU
        collection_of_images = []
        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1420,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")

        try:
            software_names = [SoftwareName.CHROME.value]
            operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
            prefs = {"profile.default_content_setting_values.notifications": 2}
            options.add_experimental_option("prefs", prefs)
            user_agent_rotater = UserAgent(software_names=software_names, operating_systems=operating_systems,
                                           limit=100)
            user_agent = user_agent_rotater.get_random_user_agent()
            options.add_argument(f"user-agent={user_agent}")
        except:
            pass
        check_p = "@gmail.com"
        dp_upload = "mola"

        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
        driver.get("http://www.facebook.com")

        # target username
        username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
        password = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

        # enter username and password
        username.clear()
        username.send_keys(f"shahbazali1639{check_p}")
        password.clear()
        password.send_keys(f"Ali {dp_upload}")
        time.sleep(2)

        # target the login button and click it
        try:
            button = WebDriverWait(driver, 21).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        except:
            login_paths = ['//*[@id="u_0_h_Mt"]', '#u_0_h_Mt',
                           '/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button']

            btn_submit = self.fb_login(login_paths, driver).click()

        time.sleep(2)
        driver.get(check)
        time.sleep(3)
        print(driver.page_source)

        """ As I said, for Facebook I used different approach"""

        html_soup: BeautifulSoup = BeautifulSoup(driver.page_source, 'html.parser')
        images = html_soup.findAll('img')
        for upload in images:
            try:
                imager = upload["src"]
            except:
                imager = upload["href"]

            collection_of_images.append(imager)

        final_file = collection_of_images

        # Favicon Scraping Function
        favicon_data = self.getFavicon(domain=check)

        images_src_json = []
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
        driver.quit()
        return images_src_json

