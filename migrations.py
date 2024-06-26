import sys
from storage.database import engine
from storage.datatypes import OrderStatus
from storage.logger import logger
from sqlalchemy import Column, MetaData, Table, BigInteger, String, Integer, DateTime, DECIMAL, Enum, func

metadata = MetaData()

users_table = Table(
  'users',
  metadata,
  Column('user_id', BigInteger, primary_key=True, autoincrement=False),
  Column('user_name', String, unique=True),
  Column('user_nickname', String, nullable=True),
)

orders_table = Table(
  'orders',
  metadata,
  Column('id', BigInteger, primary_key=True, autoincrement=False),
  Column('short', String, nullable=False),
  Column('link', String, nullable=False),
  Column('watch', Integer, default=0),
  Column('responses', Integer, default=0),
  Column('price', DECIMAL, default=0.00),
  Column('created_at', DateTime, default=func.current_timestamp()),
  Column('status', Enum(OrderStatus, name='order_status_enum', create_type=False), nullable=True)
)

def drop():
  users_table.drop(engine)
  orders_table.drop(engine)
  logger.info('Tables dropped successful.')
  
def run():
  users_table.create(engine)
  orders_table.create(engine)
  logger.info('Migrations applied.')
  
if __name__ == '__main__':
  arg = sys.argv[1]
  
  match arg:
    case 'migrate':
      run()
    case 'refresh':
      drop()
      run()
    case 'rollback':
      drop()
      