FROM python:3.11

WORKDIR /app

COPY . /app

EXPOSE 8000

ENV NAME Bot_new

ENTRYPOINT ["python", "__mainnew__.py"]
