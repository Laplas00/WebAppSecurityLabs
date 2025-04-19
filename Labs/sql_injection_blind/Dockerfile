FROM python:3.10-slim

WORKDIR /app

COPY app /app
COPY db_init.py /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["sh", "-c", "python db_init.py && python main.py"]
