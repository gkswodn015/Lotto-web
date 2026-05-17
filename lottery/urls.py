# lottery/urls.py (새 파일 생성)

from django.urls import path
from . import views

app_name = 'lottery'

urlpatterns = [
    path('buy/',        views.buy_ticket,  name='buy'),
    path('my-tickets/', views.my_tickets,  name='my_tickets'),
]