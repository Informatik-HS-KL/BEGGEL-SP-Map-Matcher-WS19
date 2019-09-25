from flask import Response, request, render_template, Blueprint

webpage = Blueprint('web', __name__)

@webpage.route('/')
def rootpage():
    return render_template('anzeige.html')
