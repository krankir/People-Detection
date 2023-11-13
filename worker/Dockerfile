FROM python:3.9

RUN mkdir /worker

WORKDIR /worker

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /worker .

ENTRYPOINT ["python", "/worker/server.py"]