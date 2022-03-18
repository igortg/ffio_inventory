from os import getenv

DATABASE_URL = getenv('DATABASE_URL', 'postgresql://postgres:masterkey@localhost/ffio_inventory')
