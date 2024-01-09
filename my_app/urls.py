from django.urls import path
from .views import start_notifier

urlpatterns = [
    path('', start_notifier, name='start_notifier'),
]
