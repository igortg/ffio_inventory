from ffio_inventory.api.app import create_app

app = create_app(db_url='postgresql://postgres:masterkey@localhost:5432/ffio_inventory-test')
