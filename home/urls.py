from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stock/<str:stock_symbol>/', views.stock, name='stock'),
    path('stock_scrape/<str:stock_symbol>/', views.stock_scrape, name='stock_scrape'),
    path('stock_scrape_json/<str:stock_symbol>/', views.stick_scrape_json, name = 'stock_scrape_json')
]
