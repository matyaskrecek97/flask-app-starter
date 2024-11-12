FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app

EXPOSE 5000

ENV FLASK_APP=/app/app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]