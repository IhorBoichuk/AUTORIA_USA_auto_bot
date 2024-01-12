from django import forms

class SearchForm(forms.Form):
    VEHICLE_TYPE_CHOICES = [
        ('Легкові', 'Легкові'),
        # Додайте інші варіанти, якщо потрібно
    ]

    vehicle_type = forms.ChoiceField(choices=VEHICLE_TYPE_CHOICES, label='Тип транспорту')
    brand_model = forms.CharField(max_length=255, label='Марка і модель')
    imported_from_us = forms.BooleanField(required=False, initial=True, label='Авто імпортовані з США')
    accident = forms.BooleanField(required=False, initial=True, label='Участь в ДТП')
