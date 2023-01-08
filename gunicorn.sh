#!/bin/sh
gunicorn -w 4 "server:create_app()" -b 0.0.0.0:80
