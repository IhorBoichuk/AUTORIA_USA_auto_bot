from django.shortcuts import render
from django.http import HttpResponse
from .utils import process_car_info
from django.shortcuts import render
from .forms import SearchForm
# from .utils import process_car_info, notify_if_new_car



# def start_notifier(request):
#     process_car_info()
#     return HttpResponse("Notifying process started.")



def start_notifier(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # Отримання даних з форми
            vehicle_type = form.cleaned_data['vehicle_type']
            brand_model = form.cleaned_data['brand_model']
            imported_from_us = form.cleaned_data['imported_from_us']
            accident = form.cleaned_data['accident']

            # Виклик функції обробки інформації
            car_info = {
                'brand': brand_model,
                'price': '15000 USD',  # Вам потрібно буде отримати цю інформацію зі свого скрапера
                'auto_ria_link': 'https://auto.ria.com',
                'auction_link': 'https://example-auction.com',
                'photo_urls': ['https://example.com/photo1.jpg', 'https://example.com/photo2.jpg', 'https://example.com/photo3.jpg']
            }
            process_car_info(car_info)

    else:
        form = SearchForm()

    return render(request, 'my_app/base.html', {'form': form})
