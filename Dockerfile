FROM python:3.8-alpine

WORKDIR /code

COPY requirements.yml .

RUN pip install -r requirements.yml

CMD ["python","app.py"]