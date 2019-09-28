from flask import Flask, Response, render_template, request

from src.rest.api import api
from src.rest.web import webpage

app = Flask(__name__)

app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(webpage, url_prefix="/")


if __name__ == '__main__':
    app.run(host="localhost", port=5000)
