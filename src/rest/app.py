from flask import Flask, Response, render_template, request, Blueprint

app = Flask(__name__)

import src.rest.api
import src.rest.web
app.register_blueprint(src.rest.web.bp_webpage, url_prefix="/")
app.register_blueprint(src.rest.api.api, url_prefix="/api")


if __name__ == '__main__':
    app.run(host="localhost", port=5000)

