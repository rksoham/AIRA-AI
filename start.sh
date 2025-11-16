#!/bin/bash

rasa train
rasa run --enable-api --cors "*" --port 8080
