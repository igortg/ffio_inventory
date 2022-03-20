FROM python:3.10.2

# Required to pip install psycopg2
RUN apt-get install -f libpq-dev

WORKDIR /opt/ffio_inventory

COPY . .

RUN pip install -r requirements.txt

RUN adduser --gecos "" ffio

ENV UPLOAD_FOLDER /mnt/ffio_uploads

VOLUME $UPLOAD_FOLDER

RUN mkdir $UPLOAD_FOLDER

RUN chown ffio $UPLOAD_FOLDER

USER ffio

COPY --chown=ffio src/ .

# CMD ["gunicorn", "ffio_inventory.api.__main__:app", "-b", "0.0.0.0:5000"]
# CMD ["python", "-m", "ffio_inventory.api"]