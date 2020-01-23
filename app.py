from flask import Flask, render_template, request, render_template_string
app = Flask(__name__)

@app.route('/')
def default():
    return render_template('form.html')