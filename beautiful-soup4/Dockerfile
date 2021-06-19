FROM python:3.8.5
WORKDIR /app/src
COPY ["/app/src/*.py", "/app/src/" ]
RUN python3 -m pip install beautifulsoup4 lxml requests python-dateutil
ENTRYPOINT [ "python3", "main.py" ]