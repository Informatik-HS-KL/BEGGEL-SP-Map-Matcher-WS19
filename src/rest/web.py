from flask import Response, request, render_template, Blueprint

webpage = Blueprint('web', __name__)

@webpage.route('/')
def root_page():
    return render_template('anzeige.html')
