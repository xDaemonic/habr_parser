import os
from eloquent import DatabaseManager, Model
from datetime import timedelta
def defineModel():
  _config = {
    'mysql': {
      'driver': 'mysql',
      'host': os.environ['DB_HOST'] or 'localhost',
      'database': os.environ['DB_DATABASE'] or 'habr_orders',
      'user': os.environ['DB_USERNAME'] or 'root',
      'password':os.environ['DB_PASSWORD'] or 'pass',
      'prefix': ''
    }
  }

  db = DatabaseManager(_config)
  Model.set_connection_resolver(db)

class Order(Model):
  __table__ = 'orders'
  __fillable__ = ['id', 'link', 'responses', 'watch', 'text', 'created', 'short']
  __timestamps__ = False
  
  def to_str(self):
    attrs = self.get_attributes()
    cr = attrs['created'].strftime('%Y-%m-%d %H:%M:%S')
    res = f'''
              <a href='{attrs['link']}'>{attrs['short']}</a><br><br>
              <b>Отклики:</b>&nbsp;{attrs['responses'] or 0}
              <b>Просмотры:</b>&nbsp;{attrs['watch'] or 0}
              <b>Создано:</b>&nbsp;{cr}
            '''
            
    print(res)
  
class User(Model):
  __table__ = 'tg_users'
  __fillable__ = [
    'id', 
    'is_bot', 
    'first_name', 
    'last_name', 
    'username', 
    'language_code', 
    'can_join_groups', 
    'can_read_all_group_messages', 
    'supports_inline_queries', 
    'is_premium', 
    'added_to_attachment_menu', 
    'can_connect_to_business'
  ]
  __timestamps__ = False