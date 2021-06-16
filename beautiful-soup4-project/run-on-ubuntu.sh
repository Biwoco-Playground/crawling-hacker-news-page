# init venv
sudo apt install -y python3-venv
mkdir venv
cd venv
python3 -m venv my-env
cd ..

# python bash
. ./python-bash.sh

# python-dateutil
python -m pip install python-dateutil

# requests
python -m pip install requests

# beautifulsoup4
python -m pip install beautifulsoup4

# lxml
python -m pip install lxml

# go to src
cd app/src

# run main
python main.py

