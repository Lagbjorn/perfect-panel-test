FROM python:3.9

EXPOSE 80

RUN pip install pipenv --no-cache-dir

WORKDIR /app/

COPY Pipfile.lock /app/Pipfile.lock
COPY Pipfile /app/Pipfile
RUN pipenv install --system --deploy --ignore-pipfile

COPY / /app/

CMD gunicorn main:app -b :80 -w 1 -k uvicorn.workers.UvicornWorker
