#!/bin/bash

# create virtual environment python
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python3 -m pip install --upgrade pip


# install necessary dependencies
 pip install -r requirements.txt

# main directory
cd App

# run app
python3 app.py
