#!/bin/bash

gunicorn -w 2 -b 0.0.0.0:4000 app:app > ../../nudedetector.log 2>&1 &
