"""
Description: Cretes Flask Application and register api and web entdpoint to this.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

from flask import Flask
import src.rest.api as api
import src.rest.web as web

app = Flask(__name__)

app.register_blueprint(web.bp_webpage, url_prefix="/")
app.register_blueprint(api.api, url_prefix="/api")

