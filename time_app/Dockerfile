FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir Flask

COPY run.py /app/run.py

EXPOSE 8080

CMD ["python", "run.py"]
