from . import app
from flask import render_template, url_for

@app.route('/')
def home():
    return app.send_static_file('index.html')
