FROM python:3.8.5
WORKDIR /app/src
COPY ["/app/src/*.py", "/app/src/" ]
RUN python3 -m pip install beautifulsoup4 requests python-dateutil && \
    python3 test_libs.py
ENTRYPOINT [ "python3", "main.py" ]