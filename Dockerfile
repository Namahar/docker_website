FROM python:3.8.12-slim

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt && apt-get update --no-install-recommends && apt-get install ffmpeg -y --no-install-recommends

EXPOSE 5000
# CMD gunicorn -b 0.0.0.0:5000 -w 2 index:app --preload
CMD gunicorn -b 0.0.0.0:$PORT -w 2 index:app --preload