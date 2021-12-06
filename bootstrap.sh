#!/bin/sh
export FLASK_APP=./pca-image/index.py
flask run -h 0.0.0.0 -p 50000
