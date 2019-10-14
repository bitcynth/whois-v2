FROM python:3.7-alpine

COPY app /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY whoisclient.py ./

EXPOSE 5000
ENTRYPOINT ["gunicorn", "-b", ":5000", "--access-logfile", "-", "--error-logfile", "-", "whoisclient:app"]