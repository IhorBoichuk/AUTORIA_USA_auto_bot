import requests
from telegram import Bot
from telegram import InputMediaPhoto, InputTextMessageContent
from .models import Car
import json
from my_project.settings import YOUR_API_KEY, API_KEY, CHAT_ID
from telegram.constants import ParseMode
import asyncio

def get_autoria_api__brand(brand):
    json_file_path = 'my_app/all_marks.json'
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    for i in data:
        if i['name']==str(brand).title():
            return i['value']

def get_autoria_api__model(brandId, model):
    api_url = f'http://api.auto.ria.com/categories/1/marks/{brandId}/models?api_key={YOUR_API_KEY}'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            all_models = response.json()
            for i in all_models:
                if i['name']==str(model).title():   
                    return i['value']
        else:
            print(f"API request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

def get_auto_ria_auto_search_result(brandId, modelId):
    url = f"https://developers.ria.com/auto/search?api_key={YOUR_API_KEY}"
    params = {
        'category_id': '1',
        'marka_id': str(brandId),
        'model_id': str(modelId),
        'matched_country': '1',
        'damage': '1'
    } 
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}  
    try:
        response = requests.get(url, params=params)
        all = response.json()
        return all['result']['search_result']
    except Exception as e:
        print(f"Error: {e}")

def get_searched_auto_detail(id_searched_auto):
    url = f"https://developers.ria.com/auto/info?api_key={YOUR_API_KEY}&auto_id={id_searched_auto}"
    try:
        response = requests.get(url)
        res = response.json()
        return (f'https://auto.ria.com/uk{res['linkToView']}', list(res['photoData'].values())[2:], res['USD'])
    except Exception as e:
        print(f"Error: {e}")

async def send_notification_to_telegram(car_info):
    bot = Bot(token=API_KEY)
    message_content = f"*{car_info['brand']}*\n\nЦіна: {car_info['price']}\n[Посилання на auto.ria]({car_info['auto_ria_link']})"
    media = [InputMediaPhoto(car_info['photo_urls'][i]) for i in range(min(3, len(car_info['photo_urls'])))]
    await bot.send_media_group(chat_id=CHAT_ID, media=media, caption=message_content, parse_mode=ParseMode.MARKDOWN)
    return    

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
        asyncio.run(send_notification_to_telegram(car_info))

def process_car_info(car_info):
    try:
        notify_if_new_car(car_info)
    except Exception as e:
        print(f"Error: {e}")
