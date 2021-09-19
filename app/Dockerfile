FROM python:3.9

ENV TZ Europe/Moscow
WORKDIR /app

# For best caching
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

CMD ["python3", "main.py"]