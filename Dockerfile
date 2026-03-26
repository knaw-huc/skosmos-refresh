FROM python:3.10

WORKDIR /app

COPY src /app/src

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
EXPOSE 80

ENTRYPOINT ["python","/app/src/refresh.py"]
