FROM python:3.12
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt pyjwt requests

COPY . /app

ENTRYPOINT ["bash", "-c", "uvicorn services_router:app --port 8080 --host 0.0.0.0"]