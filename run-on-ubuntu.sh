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

# newspaper3k
# python -m pip install newspaper3k

# beautifulsoup4
python -m pip install beautifulsoup4

# lxml
python -m pip install lxml

# scrapy
# python -m pip install scrapy

# go to src
cd app/src

# test libraries
python test_libs.py

# run main
python main.py

