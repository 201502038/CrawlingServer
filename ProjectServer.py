from flask import Flask
from flask_restful import Api
from bs4 import BeautifulSoup
import urllib.request
import requests
import json
import collections
from flask_cors import CORS

app = Flask(__name__)
api = CORS(app,resources={
  r"/review/*": {"origin": "*"},
  r"/search/*": {"origin": "*"},
})
app.config['CORS_HEADERS'] = 'application/json'
api = Api(app)

@app.route("/")
def defaultPage():
    return "<h1>Welcome to D3Project API<h1>"

@app.route("/search/<title>", methods=['GET'])
def search(title):
    client_id = "keEC3LAFtPejhNUY5Dh4"
    client_secret = "gpbNkH23IT"
    encText = urllib.parse.quote(title)
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        return response_body.decode('utf-8')


@app.route("/review/<name>", methods=['GET'])
def review(name):
    url = 'https://search.naver.com/search.naver?where=post&sm=tab_jum&query=' + name
    req = requests.get(url)
    html = req.text
    bs = BeautifulSoup(html, 'html.parser')
    img = bs.findAll('img', attrs={'class': 'sh_blog_thumbnail'})
    _title = bs.findAll('a', attrs={'class': 'sh_blog_title _sp_each_url _sp_each_title'})
    passage = bs.findAll('dd', attrs={'class': 'sh_blog_passage'})
    link = bs.findAll('a', attrs={'class': 'sp_thmb thmb80'})
    value = {
        'count': "4",
        'item': [
            {'title': _title[0]['title'], 'img': img[0]['src'], 'passage': passage[0].getText(),
             'link': link[0].get('href')},
            {'title': _title[1]['title'], 'img': img[1]['src'], 'passage': passage[1].getText(),
             'link': link[1].get('href')},
            {'title': _title[2]['title'], 'img': img[2]['src'], 'passage': passage[2].getText(),
             'link': link[2].get('href')},
            {'title': _title[3]['title'], 'img': img[3]['src'], 'passage': passage[3].getText(),
             'link': link[3].get('href')}
        ]
    }
    obj = collections.OrderedDict(value)
    jsonData = json.dumps(obj, ensure_ascii=False, sort_keys=False)
    return jsonData

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="4000")
