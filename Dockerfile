FROM python:3.6.3-alpine3.6

RUN mkdir /app

ADD requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

ADD xmr-stak-prometheus-exporter.py /app/xmr-stak-prometheus-exporter.py

EXPOSE 6132

CMD ["python", "/app/xmr-stak-prometheus-exporter.py"]
