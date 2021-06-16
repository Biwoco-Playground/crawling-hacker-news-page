# dependencies
sudo apt-get install python3 python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev

# init venv
sudo apt install -y python3-venv
mkdir venv
cd venv
python3 -m venv my-env
cd ..

# python bash
. ./python-bash.sh

# scrapy
python -m pip install scrapy