import re
from datetime import timedelta, datetime
from eloquent import Collection
from backports.zoneinfo import ZoneInfo

class ProcessPipeLine:
  _actions = []
  _data = None
  _tasks = []
  
  def __init__(self, tasks = []) -> None:
    self._tasks = tasks
    self._data = self.process()
    pass
  
  def getData(self):
    return self._data
  
  def process(self) -> list:
    formatted_tasks = []

    for task in self._tasks:
      formatted = {}
      header = task.find('header')
      if header is not None:
          link = header.find('a')
          if link is not None:
              formatted['short'] = link.text
              formatted['id'] = link['href'].split('/')[-1]
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
              time = int(re.search('[\d+]', time_string).group(0))
              dt = None
              zone = ZoneInfo("Europe/Moscow")
              if 'мин' in time_string:
                dt = datetime.now(zone) - timedelta(minutes=time)
              elif 'час' in time_string:
                dt = datetime.now(zone) - timedelta(hours=time)
              elif 'ден' in time_string or 'дня' in time_string or 'дней' in time_string:
                dt = datetime.now(zone) - timedelta(days=time)
                
              try:
                formatted['created'] = dt.strftime("%Y-%m-%d %H:%M:%S")
              except Exception as e:
                print(time, time_string)
              
          elif title == "Количество откликов":
              formatted['responses'] = span.find("i").get_text()
        
      formatted_tasks.append(formatted)
      
    return formatted_tasks