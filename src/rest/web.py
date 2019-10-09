from flask import Response, request, render_template, Blueprint

from src.rest import api
from src.map_service import MapService

bp_webpage = Blueprint('web', __name__)


@bp_webpage.route('/')
def root_page():
    return render_template('anzeige.html')

