#!/bin/bash
source entorno_virtual/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=development
flask run