#!/bin/bash

cd jstools && npm run build && cd .. && python manage.py runserver

