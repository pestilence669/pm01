#!/usr/bin/env python
# vim: set ts=4 sw=4 et fileencoding=utf-8:

from flask import Flask, jsonify, request
from src.location import *
import json
import logging
import os


app = Flask(__name__)

config_name = f'config.{os.environ.get("SETTINGS", "default").capitalize()}'
app.config.from_object(config_name)
logging.info(f'Starting with {config_name}...')

geocoder_dispatcher = GeocoderDispatcher(app.config['GEOCODING_RESOLVERS'])


###############################################################################


@app.route('/status', methods=['GET'])
def status():
    return 'ok.'


@app.route('/location/geocode', methods=['GET'])
def location_geocode():
    try:
        result = geocoder_dispatcher.resolve(request.args.get('address'))

        if result:
            return jsonify(result.__dict__)
        else:
            return 'Result not found', 404

    except Geocoder.Error as e:
        logging.exception('An error occurred geocoding.')
        return str(e), e.code


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)