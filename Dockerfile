FROM python:3.7-alpine

RUN adduser -D whois

WORKDIR /home/whois

COPY requirements.txt requirements.txt
RUN python -m venv env
RUN env/bin/pip install -r requirements.txt
RUN env/bin/pip install gunicorn

COPY app app
COPY whoisclient.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP whoisclient.py

RUN chown -R whois:whois ./
USER whois

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]