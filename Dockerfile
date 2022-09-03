FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
COPY .env /code/.env
RUN pip install -r requirements.txt
CMD /code/docker-entrypoint.sh