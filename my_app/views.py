from django.shortcuts import render
from .utils import process_car_info, get_autoria_api__model, get_autoria_api__brand, get_auto_ria_auto_search_result, get_searched_auto_detail
from django.shortcuts import render
from .forms import SearchForm
import time

def start_notifier(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            vehicle_type = form.cleaned_data['vehicle_type']
            brand_model = form.cleaned_data['brand_model']
            imported_from_us = form.cleaned_data['imported_from_us']
            accident = form.cleaned_data['accident']

            brand, model = brand_model.split()[0], brand_model.split()[1]
            brandId = get_autoria_api__brand(brand)
            modelId  = get_autoria_api__model(brandId, model)
            while True:
                search_result = get_auto_ria_auto_search_result(brandId, modelId)

                for i in range(len(search_result['ids'])):
                    autoria_links = get_searched_auto_detail(search_result['ids'][i])
                    car_info = {
                        'brand': brand_model,
                        'price': autoria_links[2],
                        'auto_ria_link': autoria_links[0],
                        'auction_link': 'https://example-auction.com',
                        'photo_urls': autoria_links[1]
                    }
                    process_car_info(car_info)
                time.sleep(600)
    else:
        form = SearchForm()

    return render(request, 'my_app/base.html', {'form': form})
