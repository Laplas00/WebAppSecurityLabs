FROM python:3.10-slim

WORKDIR /app

COPY app/main.py .
COPY app/templates ./templates

RUN pip install flask docker

EXPOSE 80
CMD ["python", "main.py"]
