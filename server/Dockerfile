FROM docker.io/library/python:3.14-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

RUN mkdir /app && \
    chown -R appuser:appgroup /app && \
    chmod 755 /app

WORKDIR /app

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    pip install --disable-pip-version-check --no-cache-dir .

COPY --chown=appuser:appgroup pyproject.toml run.py gunicorn.conf.py ./
COPY --chown=appuser:appgroup app app

USER appuser

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5000"]
