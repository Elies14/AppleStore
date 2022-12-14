FROM python:3.9-slim-bullseye

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --upgrade pip

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]
