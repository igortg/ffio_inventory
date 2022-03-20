## FFIO Inventory

A sample application that proposes an architecture to build 
Flask/Celery/SQLAlchemy that strives for maintainability and scalability.

### Launching it using Docker

Docker can be used to boot the stack. First build the app Docker image:

    docker build . -t ffio_inventory

Then start the stack with `docker-compose`:
    
    docker-compose up

The PostgreSQL container must have an empty database named `ffio_inventory`
for the app to work. Tables will be created automatically on the application
boot. Check the `prod.env` file on the repository root if you want to 
change database access parameters.


### Development

App was built with **Python 3.10**. To boot the App in development mode
first boot only required services using docker:
    
    docker-compose up -d db broker

Then `pip install` and start the Flask server:

    pip install -r requirements.txt
    export FLASK_APP=ffio_inventory.api.__main__
    flask run

Lastly, start the Celery worker:
    
    celery -A ffio_inventory.worker.app worker -l INFO

### Testing

Testing requires an empty database named `ffio_inventory_test` on Postgres.
The test suite can be started with `pytest`

    pytest tests\

Check the `tests\conftest.py` for further database configuration option.