FROM python:3.9

ENV TZ Europe/Moscow
WORKDIR /app

COPY . /app
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]