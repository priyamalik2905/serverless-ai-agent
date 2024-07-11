#!/bin/bash

deactivate  # Exit the virtual environment before packaging
zip -r deployment_package.zip list.py venv/lib/python3.9/site-packages/*
