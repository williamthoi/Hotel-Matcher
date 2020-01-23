from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)


@app.route('/')
def default():
    return render_template('form.html')


@app.route('/inputs', methods=['GET', 'POST'])
def inputs():
    if not request.form['city'] or not request.form['checkin'] or not request.form['checkout']:
        return render_template('form.html', missing=True)
    API_ENDPOINT = "https://experimentation.snaptravel.com/interview/hotels"
    snaptravel_data = {'city': request.form['city'],
                       'checkin': request.form['checkin'],
                       'checkout': request.form['checkout'],
                       'provider': 'snaptravel'}

    r = requests.post(url=API_ENDPOINT, data=snaptravel_data)
    snaptravel_data = r.json()

    retail_data = {'city': request.form['city'],
                   'checkin': request.form['checkin'],
                   'checkout': request.form['checkout'],
                   'provider': 'retail'}

    r = requests.post(url=API_ENDPOINT, data=retail_data)
    retail_data = r.json()
    data = intersect_data(snaptravel_data, retail_data)
    return render_template('demo.html', data=data)


def intersect_data(snapData, retailData):
    merged_data = []
    print(json.dumps(snapData, indent=4, sort_keys=True))
    print(json.dumps(retailData, indent=4, sort_keys=True))
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
