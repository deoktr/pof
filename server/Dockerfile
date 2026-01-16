FROM docker.io/library/python:3.14-alpine

WORKDIR /app

COPY pyproject.toml .
RUN pip3 install .

COPY gunicorn.conf.py .
COPY run.py .
COPY app app

CMD ["python3", "-m" , "gunicorn", "run:app", "-b", "0.0.0.0:5000"]
