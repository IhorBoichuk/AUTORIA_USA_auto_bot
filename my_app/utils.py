import requests
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import Bot
from telegram import InputMediaPhoto, InputTextMessageContent
from .models import Car
import time
# from telegram.ext import ParseMode


def scrape_auto_ria():
    url = "https://auto.ria.com"
    search_endpoint = "/uk/search/"
    
    params = {
        'type': '1',  # Легкові
        'marka_id': 79,  # Toyota
        'model_id': 1030,  # Sequoia
        'country': 1,  # США
        'damage': 2  # Участь в ДТП - Так
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    while True:
        try:
            response = requests.get(url + search_endpoint, params=params, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Тут ви можете реалізувати код для обробки отриманих даних, наприклад, витягти URL автомобілів із списку результатів.
            # Пам'ятайте про вивчення правил сайту auto.ria.com щодо скрапінгу.

            # Наприклад:
            # car_urls = [car['href'] for car in soup.find_all('a', class_='link-top')]

            # Тут можна викликати функцію для обробки URL автомобілів або збереження даних у базу даних.

        except Exception as e:
            print(f"Error: {e}")

def send_notification_to_telegram(car_info):
    bot_token = '6466822049:AAFsHi9pzmS5t_2IIvPBJglrq-nSAOMmVFE'
    chat_id = ' -1001644481765'
    bot = Bot(token=bot_token)

    # Формування повідомлення
    message_content = f"*{car_info['brand']}*\n\nЦіна: {car_info['price']}\n[Посилання на auto.ria]({car_info['auto_ria_link']})\n[Посилання на аукціон]({car_info['auction_link']})"
    print(message_content)
    # Додавання фотографій у вигляді альбому
    media = [InputMediaPhoto(car_info['photo_urls'][i]) for i in range(min(3, len(car_info['photo_urls'])))]
    
    # Надсилання повідомлення
    bot.send_media_group(chat_id=chat_id, media=media, caption=message_content, )#parse_mode=ParseMode.MARKDOWN

def notify_if_new_car(car_info):
    try:
        car = Car.objects.get(auto_ria_link=car_info['auto_ria_link'])
    except Car.DoesNotExist:
        car = Car.objects.create(
            brand=car_info['brand'],
            price=car_info['price'],
            auto_ria_link=car_info['auto_ria_link'],
            auction_link=car_info['auction_link'],
            photo_urls=car_info['photo_urls']
        )
        send_notification_to_telegram(car_info)

def process_car_info(car_info):
    while True:
        try:
            car_info = car_info
            '''{
                'brand': 'Toyota Sequoia',
                'price': '15000 USD',
                'auto_ria_link': 'https://auto.ria.com',
                'auction_link': 'https://example-auction.com',
                'photo_urls': ['https://example.com/photo1.jpg', 'https://example.com/photo2.jpg', 'https://example.com/photo3.jpg']
            }'''
            

            notify_if_new_car(car_info)

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(600)  # Затримка 10 хвилин перед наступним запитом
