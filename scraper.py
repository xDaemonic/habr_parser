import requests, lxml, os
import telebot
from bs4 import BeautifulSoup
from src.models import defineModel, Order
from src.process import ProcessPipeLine
from dotenv import load_dotenv

load_dotenv()
defineModel()

# for order in Order.all():
#   print(order.to_str())
#   exit(200)


url = 'https://freelance.habr.com/tasks?categories=development_all_inclusive%2Cdevelopment_backend%2Cdevelopment_frontend%2Cdevelopment_prototyping%2Cdevelopment_ios%2Cdevelopment_android%2Cdevelopment_desktop%2Cdevelopment_bots%2Cdevelopment_games%2Cdevelopment_1c_dev%2Cdevelopment_scripts%2Cdevelopment_voice_interfaces%2Cdevelopment_other'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

tasks_list = soup.find('ul', id='tasks_list')
tasks = tasks_list.find_all('li', class_='content-list__item')
processor = ProcessPipeLine(tasks=tasks)
formatted_tasks = processor.getData()
formatted_tasks.sort(key=lambda x: x['created'], reverse=True)

print(formatted_tasks[0])
exit(200)

for task in formatted_tasks:
  if not Order.where_id(task['id']).exists():
    text_page = requests.get(task['link'])
    soup = BeautifulSoup(text_page.text, 'lxml')
    task['text'] = soup.find('div', class_='task__description').text
    task_model = Order.create(**task)
    
    exit(200)
  # Order.first_or_create()
  
# ids = list(map(lambda x: x['id'], formatted_tasks))
# data = Order.where_not_in('id', tuple(ids)).get()