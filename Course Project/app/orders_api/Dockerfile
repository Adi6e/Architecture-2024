FROM python:3.12
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["bash", "-c", "uvicorn orders_router:app --port 8080 --host 0.0.0.0"]