FROM alpine:latest

WORKDIR /app

ADD . /app

ENTRYPOINT [ "test_openai.py" ]