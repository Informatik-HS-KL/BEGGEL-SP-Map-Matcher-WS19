"""
Description: Todo
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""


from flask import Flask, Response, render_template, request, Blueprint
import src.rest.api
import src.rest.web

app = Flask(__name__)

app.register_blueprint(src.rest.web.bp_webpage, url_prefix="/")
app.register_blueprint(src.rest.api.api, url_prefix="/api")

