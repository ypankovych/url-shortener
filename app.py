import os

from flask import Flask, redirect, render_template
from flask_restful import Api
from webargs.flaskparser import parser, abort

from models import Url
from resources.Short import ShortUrl

app = Flask(__name__)
api = Api(app)


@parser.error_handler
def handle_request_parsing_error(err, req, schema):
    abort(422, errors=err.messages)


@app.route('/<path:short>')
def do_redirect(short):
    url = Url.get_base_by_short(short)
    if url:
        return redirect(url.base_url, code=302)
    abort(404)


@app.errorhandler(404)
def return_404(error):
    print(error)
    return render_template('404_error.html'), 404


@app.route('/')
def index():
    return render_template('index.html')


api.add_resource(ShortUrl, '/short')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT'))
