from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
  data = [{
    'name': '1'
  }, {
    'name': '2'
  }]
  return render_template('demo.html', name='world', data=data)