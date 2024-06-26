import requests, lxml, os, re, pytz, time
from bs4 import BeautifulSoup
from fake_headers import Headers
from datetime import timedelta, datetime
from bs4.element import ResultSet
from models import Order
from storage.datatypes import OrderStatus

class HabrParser:
  
  _url = 'https://freelance.habr.com/tasks?categories=development_all_inclusive%2Cdevelopment_backend%2Cdevelopment_frontend%2Cdevelopment_prototyping%2Cdevelopment_ios%2Cdevelopment_android%2Cdevelopment_desktop%2Cdevelopment_bots%2Cdevelopment_games%2Cdevelopment_1c_dev%2Cdevelopment_scripts%2Cdevelopment_voice_interfaces%2Cdevelopment_other'
  _headers = None
  _refound = 10
  _headers = Headers(browser='chrome', os='mac', headers=True).generate()
  
  @classmethod
  def get_soup(cls, text):
    return BeautifulSoup(text, 'lxml')

  @classmethod
  def get_html(cls, page: int = None):
    page_url = cls._url if page == None else f"{cls._url}&page={page}"
    return requests.get(page_url, headers=cls._headers).text

  @classmethod
  def run(cls):
    current = 1
    formatted_tasks = []
    while current <= cls._refound:
      page = (current if current > 0 else None)
      html = cls.get_html(page=page)
      soup = cls.get_soup(text=html)
    
      tasks_list = soup.find('ul', id='tasks_list')
      tasks = tasks_list.find_all('li', class_='content-list__item')
      processor = TasksProcessor(tasks)
      formatted_tasks += processor.getData()
      
      current += 1
  
    for order in formatted_tasks:
      order_model = Order.updateOrCreate(attrs=order, upd=['watch', 'responses'])
      if order_model.getAttribute('status') is None:
        order_model.setAttribute('status', OrderStatus.NEW)
        order_model.update()
      
# for task in formatted_tasks:
#   if not Order.where_id(task['id']).exists():
#     text_page = requests.get(task['link'])
#     soup = BeautifulSoup(text_page.text, 'lxml')
#     task['text'] = soup.find('div', class_='task__description').text
#     Order.create(**task)
  
#   task_model = Order.find(task['id'])
#   message_str = task_model.to_str()
#   print(message_str)
#   exit(200)
  
# ids = list(map(lambda x: x['id'], formatted_tasks))
# data = Order.where_not_in('id', tuple(ids)).get()

class TasksProcessor:
  _data = None
  _actions: list = []
  _tasks: list = []
  
  def __init__(self, tasks: ResultSet) -> None:
    self._tasks = tasks
    self._data = self.process()
    pass
  
  def getData(self) -> list:
    return self._data
  
  def process(self) -> list:
    formatted_tasks = []

    for task in self._tasks:
      formatted = {}
      
      header = task.find('header')
      if header is not None:
          link = header.find('a')
          if link is not None:
              formatted['id'] = link['href'].split('/')[-1]
              formatted['short'] = link.text
              formatted['link'] = f"https://freelance.habr.com{link['href']}"
              
      task_params = task.find("div", class_="task__params")
      if task_params is not None:
        spans = task_params.children
        spans = list(filter(lambda x: x is not None and x.name == 'span', spans))
        
        for span in spans:
          title = span['title']
          
          if title == "Количество просмотров заказа за месяц":
              formatted['watch'] = span.find("i").get_text()
              
          elif title == "Дата публикации заказа":
              time_string = span.get_text().strip()
              time = int(re.search(r'[\d+]', time_string).group(0))
              dt = None
              tz = pytz.timezone('Europe/Moscow')
              if 'мин' in time_string:
                dt = datetime.now(tz) - timedelta(minutes=time)
              elif 'час' in time_string:
                dt = datetime.now(tz) - timedelta(hours=time)
              elif 'ден' in time_string or 'дня' in time_string or 'дней' in time_string:
                dt = datetime.now(tz) - timedelta(days=time)
                
              try:
                formatted['created_at'] = dt.strftime("%Y-%m-%d %H:%M:%S")
              except Exception as e:
                print(time, time_string)
              
          elif title == "Количество откликов":
              formatted['responses'] = span.find("i").get_text()
      
      task_price = task.find('div', class_='task__price')
      if task_price is not None:
        nego = task_price.find('span', class_='task_price')
        if nego is not None:
          formatted['price'] = 0
        else:
          price = task_price.find('span', class_='count')
          if price is not None:
            price_str = ' '.join([el.text for el in price.children]).replace(' ', '') if price is not None else 0
            price = re.search(r'[\d]+', price_str).group(0)
          else:
            price = 0
          
          formatted['price'] = int(price)
      
      formatted_tasks.append(formatted)
      
    return formatted_tasks
  
  
  