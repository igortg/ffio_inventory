from ffio_inventory.api.app import create_app
import os

env = os.environ.get

DATABASE_URL = env('DATABASE_URL', 'postgresql://postgres:masterkey@localhost/ffio_inventory')

app = create_app(db_url=DATABASE_URL)

if __name__ == '__main__':
    app.run()
