import requests
from flask import jsonify
from flask import Flask, Response, request, render_template
app = Flask(__name__)

@app.route('/')
def rootpage():
    return render_template('anzeige.html')

@app.route('/tile/locations/')
def get_locations():
    """
    :return:
    """

    return

@app.route('/ways')
def get_ways():
    """"""


    return render_template('anzeige.html', name="TEST", data = data)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
