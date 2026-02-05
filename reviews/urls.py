from django.urls import path
from . import views

# app_name помогает различать URL разных приложений
app_name = 'reviews'

# Список маршрутов
urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
]
