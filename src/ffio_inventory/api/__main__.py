from ffio_inventory.api.app import create_app

from ffio_inventory.repository import DATABASE_URL

app = create_app(db_url=DATABASE_URL)

if __name__ == '__main__':
    app.run()
