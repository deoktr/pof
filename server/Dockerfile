FROM docker.io/library/python:3.13-alpine

WORKDIR /app

COPY pyproject.toml .
RUN pip3 install .

COPY . .

CMD ["python3", "-m" , "gunicorn", "app:app", "-b", "0.0.0.0:5000"]
