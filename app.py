from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint

from facebook_scrapper import Facebook_scrapper
from main import Scrapper
from youtube_scrapper import Youtube_Scrapper

app = Flask(__name__)
api = Api(app)

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

class Hello(Resource):
    def get(self):
        baseUrl = request.args.get("URL")
        baseUrl = validate_url(baseUrl)
        if "youtube" in baseUrl:
            response = Youtube_Scrapper().decision("https://www.youtube.com")
        elif "facebook" in baseUrl:
            response = Facebook_scrapper().decision("https://www.facebook.com")
        else:
            response = Scrapper().get_all(baseUrl)
        return jsonify(response)



api.add_resource(Hello, '/Fetch_images')

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
