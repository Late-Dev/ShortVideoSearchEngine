FROM python:3.11

COPY requirements.txt /

RUN pip install -U pip 
RUN pip install -r requirements.txt --no-cache-dir

COPY . /

ENTRYPOINT [ "bash", "run_server.sh" ]