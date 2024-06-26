from decouple import config
from storage.logger import logger
from sqlalchemy import create_engine

engine = create_engine(f"postgresql+psycopg2://{config('DB_USERNAME')}:{config('DB_PASSWORD')}@{config('DB_HOST')}/{config('DB_DATABASE')}")
if engine: logger.info('Database engine created!')