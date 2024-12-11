FROM python:3.13

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt \
	&& ./setup.py install

ENTRYPOINT ["pof"]
