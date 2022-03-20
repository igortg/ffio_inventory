from os import getenv

DATABASE_URL = getenv(
    'FFIO_DATABASE_URL', 'postgresql://postgres:masterkey@localhost/ffio_inventory'
)
