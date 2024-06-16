FROM python:3.11

WORKDIR /controller

COPY requirements.txt $WORKDIR

RUN pip install -r requirements.txt --no-cache

COPY . $WORKDIR

ENTRYPOINT [ "bash", "start.sh" ]
