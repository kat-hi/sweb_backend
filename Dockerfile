# server setup
FROM python:3.6

COPY . SWEB_APP/
WORKDIR SWEB_APP

RUN chmod +x requirements.txt

RUN pip install -r requirements.txt --no-cache-dir --compile

ENV FLASK_ENV="production"

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/SWEB_APP/sweb_backend/
EXPOSE 5000

WORKDIR sweb_backend/

CMD ["flask", "run", "--host","0.0.0.0"]
