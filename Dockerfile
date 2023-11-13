FROM python:3.9

RUN mkdir /src

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pip install gunicorn
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN chmod a+x /src/docker/*.sh

CMD ["gunicorn", "main:app", "--workers 4", "--worker-class uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
