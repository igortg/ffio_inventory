from sqlalchemy import MetaData, Table, Column, String

metadata = MetaData()

product_table = Table(
    'product',
    metadata,
    Column('name', String()),
    Column('sku', String()),
    Column('description', String()),
)
