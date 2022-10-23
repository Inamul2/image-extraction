from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
import validators
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests


class Scrapper:

    def getFavicon(self, domain):
        page = requests.get(domain)
        soup = BeautifulSoup(page.text, 'html.parser')
        icon_link = soup.find("link", rel="shortcut icon")
        if icon_link is None:
            icon_link = soup.find("link", rel="icon")
        if icon_link is None:
            return [domain + '/favicon.ico']
        return [icon_link["href"]]

    def scraping_strategy(self, check):
        """
        This Function is most advance function to scrape
        data from almost any website. - 100000 websites are tested
        """
        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        if "airbnb" not in check:
            user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 ' \
                         'Safari/537.2 '
            options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

        driver.get(check)
        time.sleep(5)
        ar = driver.page_source
        print(ar)
        last_height = driver.execute_script("return document.body.scrollHeight")
        if last_height != 0:
            try:
                move_on = int(last_height) / 4
                driver.execute_script(f"window.scrollTo(0, {move_on})")
                time.sleep(0.5)
                driver.execute_script(f"window.scrollTo({move_on}, {move_on * 2})")
                time.sleep(0.5)
                driver.execute_script(f"window.scrollTo({move_on * 2}, {move_on * 3})")
                time.sleep(0.5)
                driver.execute_script(f"window.scrollTo({move_on * 3}, {move_on * 4})")
                time.sleep(1.5)
                print(last_height)
            except:
                pass
        else:
            try:
                for scrolling in range(4):
                    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.5)
            except:
                pass

        if "amazon." in check:
            try:
                from selenium.webdriver.common.action_chains import ActionChains

                clicker_op = driver.find_elements(By.XPATH,
                    '//li[@class="a-spacing-small item imageThumbnail a-declarative"]/span/span/span/input')
                for clicking in clicker_op:
                    hover = ActionChains(driver).move_to_element(clicking)
                    hover.perform()
            except:
                pass

        time.sleep(5)
        r = driver.page_source

        soup = BeautifulSoup(r, "html.parser")
        images = soup.findAll('img')
        check_tags = ['picture', 'figure', 'image']
        all_data = []
        complete_images = []

        for image in images:
            try:
                a = image["src"]
            except:
                pass
            try:
                a = image["href"]
            except:
                pass

            try:
                domain = urlparse(check).netloc
                if validators.url(f"http:/{a}") is True:
                    complete_images.append(f"https:/{a}")

                elif validators.url(f"http:{a}") is True:
                    complete_images.append(f"https:{a}")
                elif validators.url(a) is True:
                    complete_images.append(a)

                elif validators.url(f"https://{a}") is True:
                    complete_images.append(f"https://{a}")
                elif validators.url(f"http://{domain + a}") is True:
                    complete_images.append(f"https://{domain + a}")
                else:
                    complete_images.append(a)
            except:
                pass
        try:
            for tag in check_tags:
                try:
                    find_tag = driver.find_elements(By.TAG_NAME, tag)
                    if len(find_tag) != 0:
                        for append in find_tag:
                            all_data.append(append)
                except:
                    pass
            for single_element in all_data:
                image = single_element.get_attribute("href")
                if type(image) == type(None):
                    image = single_element.get_attribute("src")
                    if type(image) == type(None):
                        image = single_element.value_of_css_property("background-image")
                        if image == "none":
                            sorry = 0
                        else:
                            this_image = str(image).split('"')

                            complete_images.append(this_image[1])


                    else:
                        complete_images.append(image)
                else:
                    complete_images.append(image)
        except:
            pass

        final_file = complete_images
        favicon_data = self.get_favicons(check, driver)
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

    def get_favicons(self, check, driver):
        """
        This function will scrape the favicons of the website.
        :param check: WEBSITE DOMAIN LINK
        :param driver: SELENIUM WEB DRIVER
        :return: FAVICONS LIST
        """
        all_favicons = []
        domain1 = f"http://{str(urlparse(check).netloc)}/favicon.ico"
        domain2 = f"https://{str(urlparse(check).netloc)}/favicon.ico"

        if validators.url(domain1) is True:
            all_favicons.append(domain1)
        elif validators.url(domain2) is True:
            all_favicons.append(domain2)

        all_favicons.append(domain1)

        try:
            fav = driver.find_element(By.XPATH, '//link[@rel="shortcut icon"]')

            fav = fav.get_attribute("href")

            all_favicons.append(fav)
        except:
            pass

        return all_favicons

    def get_all(self, url):

        try:
            try:
                req = Request(url)
                html_page = urlopen(req)
                soup = BeautifulSoup(html_page, "html.parser")
                links = []
                for link in soup.findAll('img'):
                    links.append({"URL" : url + link.get('src')})

                for fav in self.getFavicon(url):
                    if url in fav:
                        links.append({"Favicon": fav})
                    else:
                        links.append({"Favicon": url + fav})

                return {"Success": True, "Data Scraped": links, "Status Code": 200}
            except:
                return {"Success": True, "Data Scraped": self.scraping_strategy(url), "Status Code": 200}
        except Exception:
            return {"Success": False, "Message": "Some Internal Issue has been occured", "Status Code": 500}
