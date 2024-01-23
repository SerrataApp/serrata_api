FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8080

LABEL authors="Tang0Ch4rlie"

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8080"]
