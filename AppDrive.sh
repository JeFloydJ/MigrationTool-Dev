#!/bin/bash

# Install Homebrew if not installed
if ! command -v brew &> /dev/null; then
    echo "Install Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
 
# config project and install python
echo "make source to profile..."
source source ~/.zshrc

#install python3 
if ! command -v python3 &> /dev/null; then
    echo "Install Python3 with Homebrew..."
    brew install python3
fi

# update system path
echo "update source..."
source source ~/.zshrc

#create alias for pip3
alias pip=pip3

echo "source update..."
source source ~/.zshrc

rm -rf __MACOSX
rm -rf MigrationTool-main
rm -rf MigrationTool.zip
rm -rf test

# Install gdown 
if ! command -v gdown &> /dev/null; then
    echo "Install gdown..."
    pip install gdown
fi

FILEID=1NWmoWcbGYlCFEaxtd4-NC-huOAbr0XjD
FILENAME=MigrationTool-main.zip

#download project
if [ ! -f "$FILENAME" ]; then
    echo "Downloading $FILENAME..."
    gdown --id $FILEID --output $FILENAME
else
    echo "$FILENAME doesnt exist. No need to download."
fi

# unzip project
if [ ! -d "test" ]; then
    echo "un $FILENAME..."
    unzip $FILENAME
else
    echo "folder already exists."
fi

cd MigrationTool-main

# create virtual environment
if [ ! -d "venv" ]; then
    echo "creanting virtual enviroment..."
    python3 -m venv venv
else
    echo "virtual enviroments exists."
fi

# activate virtual environment
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

cd App

# run App
python3 app.py
