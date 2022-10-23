import validators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from urllib.parse import urlparse
import time
import os
from flask import Flask, request, jsonify
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from urllib.request import Request, urlopen
import requests
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint


# # Google sheet requirements to upload get 100000 tests results
# sa = gspread.service_account(filename="advance.json")
# sh = sa.open("ORI- Advance Scraper")
# wks = sh.worksheet("Sheet1")
#
#
# class TodoResponseSchema(Schema):
#     """
#     Class to define fields which will use in swagger API.
#     """
#     URL = fields.Str()
#     Favicon = fields.Str()
#
#
# class TodoListResponseSchema(Schema):
#     """
#     Class that join and adjust the view of output results of scraper.
#     """
#     Data_Scraped = fields.List(fields.Nested(TodoResponseSchema))


def get_favicons(check, driver):
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


# def fb_login(fb_paths, driver):
#     """
#     Facebook is hard to scrape, We have to use some advance techniques
#     to scrape data - This function will help to login.
#     """
#     try:
#         entry_input = driver.find_element_by_xpath(fb_paths[0])
#     except:
#         try:
#             entry_input = driver.find_element_by_xpath(fb_paths[2])
#         except:
#             entry_input = driver.find_element_by_css_selector(fb_paths[1])
#
#     return entry_input

def facebook_scraper(check):
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

        # btn_submit = self.fb_login(login_paths, driver).click()

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
    favicon_data = getFavicon(domain=check)

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


def youtube_killer(check):
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
        driver.get(check)
        time.sleep(5)
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(5)
        total_elements = driver.find_elements(By.XPATH, '//*[@id="img"]')
        for check_elem in total_elements:
            get_elem = str(check_elem.get_attribute("src"))
            if ".com" in get_elem:
                collection_of_images.append(get_elem)

        final_file = collection_of_images
        favicon_data = getFavicon(check)
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


def scraping_strategy(check):
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
    favicon_data = get_favicons(check, driver)
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


def validate_url(url):
    if 'http' in url and "www" not in url:
        url = url.split("//")[-1]

    if "www." not in url:
        url = "www." + url
    if "http" not in url:
        url = "https://" + url
    if "https" not in url:
        url = "https://" + url
    return url


def getFavicon1(domain):
        page = requests.get(domain)
        soup = BeautifulSoup(page.text, 'html.parser')
        icon_link = soup.find("link", rel="shortcut icon")
        if icon_link is None:
            icon_link = soup.find("link", rel="icon")
        if icon_link is None:
            return [domain + '/favicon.ico']
        return [icon_link["href"]]


def getFavicon(domain):
    favicons = getFavicon1(domain)
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


class Fetch_images(Resource):
    def get(self):
        baseUrl = request.args.get("URL")
        baseUrl = validate_url(baseUrl)
        if "youtube" in baseUrl:
            try:
                links = youtube_killer(baseUrl)
                response = {"Success": True, "Data Scraped": links, "Status Code": 200}
            except Exception as e:
                response = {"Success": False, "Message": "Some Internal Issue has been occured - " + str(e),
                            "Status Code": 500}
            return response

        elif "facebook" in baseUrl:
            try:
                links = facebook_scraper(baseUrl)
                response = {"Success": True, "Data Scraped": links, "Status Code": 200}
            except Exception as e:
                response = {"Success": False, "Message": "Some Internal Issue has been occured - " + str(e),
                            "Status Code": 500}
            return response

        else:
            try:
                try:
                    req = Request(baseUrl)
                    html_page = urlopen(req)
                    soup = BeautifulSoup(html_page, "html.parser")
                    links = []
                    for link in soup.findAll('img'):
                        links.append({"URL": baseUrl + link.get('src')})

                    for fav in getFavicon(baseUrl):
                        if baseUrl in fav:
                            links.append({"Favicon": fav})
                        else:
                            links.append({"Favicon": baseUrl + fav})

                    response = {"Success": True, "Data Scraped": links, "Status Code": 200}
                except:
                    response = {"Success": True, "Data Scraped": scraping_strategy(baseUrl), "Status Code": 200}
            except Exception:
                response = {"Success": False, "Message": "Some Internal Issue has been occured", "Status Code": 500}

            return response


# __________________________

app = Flask(__name__)
api = Api(app)

api.add_resource(Fetch_images, '/Fetch_images')

SWAGGER_URL = '/api/docs'
API_URL = '/static/openapi.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flasgger"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# driver function
if __name__ == '__main__':
    app.run()
