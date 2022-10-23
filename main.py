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

    def get_all(self, url):

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
        except Exception:
            return {"Success": False, "Message": "Some Internal Issue has been occured", "Status Code": 500}
