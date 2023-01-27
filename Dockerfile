FROM python:3.9
WORKDIR ./
COPY ./requirement.txt ./requirement.txt
RUN pip install -r requirement.txt
COPY ./kafka_consumer_flask.py ./kafka_consumer_flask.py
CMD ["python3","./kafka_consumer_flask.py"]
