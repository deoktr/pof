FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt

ADD . .

ENTRYPOINT ["python", "pof.py"]
