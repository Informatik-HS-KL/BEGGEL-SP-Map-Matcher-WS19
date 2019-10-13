from flask import Response, request, render_template, Blueprint

webpage = Blueprint('web', __name__)

@webpage.route('/')
def root_page():

    return render_template('anzeige.html')

# Client Daten erfassen
#@webpage.route('/client')
#def clientinfo():
#    data = request.args.get("data")
#    print(data)
#    return "OK"
