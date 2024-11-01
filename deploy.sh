#!/bin/bash

gunicorn -w 2 -b 0.0.0.0:5000 app:app > ../../nudedetector.log 2>&1 &
