from flask import Flask, render_template, request
from flask_caching import Cache

import requests
import json
cache = Cache(config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 20})

app = Flask(__name__)

cache.init_app(app)


@app.route('/')
def default():
    return render_template('form.html')


@app.route('/results', methods=['POST'])
def results():
    if not request.form['city'] or not request.form['checkin'] or not request.form['checkout']:
        return render_template('form.html', missing=True)
    data = cache.get(
        request.form['city'] + request.form['checkin'] + request.form['checkout'])
    if not data:
        API_ENDPOINT = "https://experimentation.snaptravel.com/interview/hotels"
        snaptravel_data = {'city': request.form['city'],
                           'checkin': request.form['checkin'],
                           'checkout': request.form['checkout'],
                           'provider': 'snaptravel'}

        r = requests.post(url=API_ENDPOINT, data=snaptravel_data)
        if r.status_code == 200:
          snaptravel_data = r.json()
        else:
          return render_template('form.html', api_error=True)

        retail_data = {'city': request.form['city'],
                       'checkin': request.form['checkin'],
                       'checkout': request.form['checkout'],
                       'provider': 'retail'}

        r = requests.post(url=API_ENDPOINT, data=retail_data)
        if r.status_code == 200:
          retail_data = r.json()
        else:
          return render_template('form.html', api_error=True)

        data = intersect_data(snaptravel_data, retail_data)
        cache.set(
            request.form['city'] + request.form['checkin'] + request.form['checkout'], data)

    return render_template('demo.html', data=cache.get(request.form['city'] + request.form['checkin'] + request.form['checkout']))


def intersect_data(snapData, retailData):
    merged_data = []
    for snapItem in snapData["hotels"]:
        for retailitem in retailData["hotels"]:
            if snapItem["id"] == retailitem["id"]:
                merged_data.append({
                    "address": snapItem["address"],
                    "amenities": snapItem["amenities"],
                    "hotel_name": snapItem["hotel_name"],
                    "id": snapItem["id"],
                    "image_url": snapItem["image_url"],
                    "num_reviews": snapItem["num_reviews"],
                    "num_stars": snapItem["num_stars"],
                    "snap_price": snapItem["price"],
                    "retail_price": retailitem["price"],
                })
    return merged_data
