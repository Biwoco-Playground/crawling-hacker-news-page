FROM python:3.8.5
WORKDIR /Articles
COPY ["requirements.txt", "/Articles/*.py", "/Articles/"]
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3", "main.py" ]