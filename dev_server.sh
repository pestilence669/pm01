#!/bin/bash
# vim: set ts=4 sw=4 noet fileencoding=utf-8:

export FLASK_DEBUG=1
export FLASK_APP=main.py
export PYTHONPATH='src'
export SETTINGS=dev
flask run
