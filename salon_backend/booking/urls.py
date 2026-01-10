from django.urls import path
from .views import book_appointment, success

urlpatterns = [
    path('', book_appointment, name='book'),
    path('success/', success, name='success'),
]

