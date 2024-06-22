from src.Connection import Connection
from dotenv import load_dotenv

load_dotenv()

conn = Connection()
table_orders = '''CREATE TABLE IF NOT EXISTS orders (
    id INT(11) UNSIGNED PRIMARY KEY,
    link VARCHAR(255) NOT NULL,
    responses INT(11) UNSIGNED,
    watch INT(11) UNSIGNED,
    short VARCHAR(255),
    text TEXT,
    created DATETIME,
    dt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
  )'''
  
conn.query(table_orders)

table_users = '''CREATE TABLE IF NOT EXISTS tg_users(
    id INT(11) UNSIGNED PRIMARY KEY,
    is_bot TINYINT,
    first_name VARCHAR(255),
    last_name VARCHAR(255), 
    username VARCHAR(255),
    language_code VARCHAR(255),
    can_join_groups VARCHAR(255),
    can_read_all_group_messages VARCHAR(255),
    supports_inline_queries VARCHAR(255),
    is_premium VARCHAR(255),
    added_to_attachment_menu VARCHAR(255),
    can_connect_to_business VARCHAR(255)
  )'''
  
conn.query(table_users)