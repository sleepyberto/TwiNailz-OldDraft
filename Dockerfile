FROM python:3.11-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt 

RUN pip install openai

CMD [ "python", "test_openai.py" ]