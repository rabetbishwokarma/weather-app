FROM alpine:latest
WORKDIR /app

RUN set -ex && \
    apk --no-cache add python3 py3-pip tini && \
    python3 -m venv venv_weather && \
    source venv_weather/bin/activate && \
    pip install --upgrade pip setuptools-scm

COPY requirements.txt /app/

RUN python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    addgroup -g 1000 appuser && \
    adduser -u 1000 -G appuser -D -h /app appuser && \
    chown -R appuser:appuser /app


USER appuser
EXPOSE 8000/tcp
ENTRYPOINT ["tini", "--"]
CMD ["python", "/app/main/manage.py", "runserver", "0.0.0.0:8000"]
