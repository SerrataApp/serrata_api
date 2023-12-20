FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

ENV SECRET_KEY_JWT=131b1fc44d874833d8e828189c9370475013d5d23bf437dafb6d22ab700efa7c \
    ALGORITHM=HS256 \
    ACCESS_TOKEN_EXPIRE_MINUTES=30 \
    SEL=lescroissantscestsuperbon

LABEL authors="Tang0Ch4rlie"

CMD ["uvicorn", "app.api:app", "--host", "127.0.0.1", "--port", "8000"]
