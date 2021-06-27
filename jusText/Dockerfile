FROM python:3.8.5
WORKDIR /jusText
COPY ["requirements.txt", "/jusText/*.py", "/jusText/" ]
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3", "main.py" ]