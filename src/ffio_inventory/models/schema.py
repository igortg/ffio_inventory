from sqlalchemy import MetaData, Table, Column, String, Integer

metadata = MetaData()

product_table = Table(
    'product',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('sku', String),
    Column('name', String),
    Column('description', String),
)
