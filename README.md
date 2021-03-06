# Fullstack Demo
The initial template was forked from: https://gitlab.com/snaptravel/full-stack-demo
## What I added

Implemented a simple flask web app that serves html.

If you are unfamiliar with flask the documentation can be found here

https://flask.palletsprojects.com/en/1.1.x/#user-s-guide

but the flask boilerplate is provided to you in this demo. Please add your service code in the @app.route('/') endpoint in app.py. The HTML should be added to templates/demo.html.

Any new dependencies should be added to requirements.txt

To run the service please cd into your local repo directory and run:
```
pip install -r requirements.txt
export FLASK_APP=app.py
python -m flask run
```

The service will be running at http://127.0.0.1:5000/.

**Step 1**

The app should load a form with the following fields
- City string input
- Checkin string input
- Checkout string input
- submit button

The 3 inputs will be string inputs.

**Step 2**

When the form is submitted make **2 HTTP POST requests** to 'https://experimentation.snaptravel.com/interview/hotels' with the following request body

```
{
  city : city_string_input,
  checkin : checkin_string_input,
  checkout : checkout_string_input,
  provider : 'snaptravel'
}
```

1) The above returns SnapTravel rates for hotels in the city

```
{
  city : city_string_input,
  checkin : checkin_string_input,
  checkout : checkout_string_input,
  provider : 'retail'
}
```

2) The above returns Hotels.com rates for hotels in the city

The responses will be in json and each response will have an array of hotels and prices.
```
[{
  id : 12,
  hotel_name : 'Center Hilton',
  num_reviews : 209,
  address : '12 Wall Street, Very Large City',
  num_stars : 4,
  amenities : ['Wi-Fi', 'Parking'],
  image_url : 'https://images.trvl-media.com/hotels/1000000/20000/19600/19558/19558_410_b.jpg',
  price : 132.11
},
...
]
```

Cached these responses in the server (assumed the endpoint is expensive to call)with Flask_Cache

**Step 3**

After both these calls have returned take **only** the hotels that appear in both the responses and return an html table with the data. 

For example, if the first call returned hotels with id [10,12] with SnapTravel prices 192.34 and 112.33 and the second call returned hotels [12,13] with Hotels.com prices 132.11 and 321.62 respectively, the form would only render hotel 12 in the list with a SnapTravel price of 112.33 and a Hotels.com price of 132.11

