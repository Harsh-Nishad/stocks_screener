from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stock/<str:stock_symbol>/', views.stock_db, name='stock_db'),
    path('suggestions/', views.stock_suggestions, name='stock_suggestions'),
]
