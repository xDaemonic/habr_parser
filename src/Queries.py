import mysql.connector, os
from src.Connection import Connection

class Queries:
  
  db = None
  
  def __init__(self) -> None:
    self.db = Connection()
  # def connect(self) -> bool:
  #   try:
  #     self.db = mysql.connector.connect(
  #       host=os.environ['DB_HOST'] or 'localhost',
  #       user=os.environ['DB_USERNAME'] or 'user',
  #       password=os.environ['DB_PASSWORD'] or 'pass',
  #       database=os.environ['DB_DATABASE'] or ''
  #     )
  #     return True
  #   except Exception as e:
  #     print("Ошибка подключения:", e)
  #     exit(200)
  #     return False
    

  def getOrdersById(self, ids: list):
    safe_args = ''.join('%s, ' * len(ids))[:-2]
    # print(safe_args, len(safe_args))
    query = f"SELECT * FROM habr_orders WHERE id IN ({safe_args})"
    # print(query)
    # exit(200)
    args=tuple(ids)
    # print(args, len(args))
    # exit(200)
    r = self.db.query(query, args)
    print(r)
    exit(200)
  