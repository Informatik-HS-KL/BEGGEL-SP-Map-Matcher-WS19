"""
Description: Main Entdpoints for HTML Delivery an web Frontend
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""


from flask import render_template, Blueprint

bp_webpage = Blueprint('web', __name__)


@bp_webpage.route('/')
def root_page():

    return render_template('anzeige.html')
