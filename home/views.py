from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .insert_db import get_one_stock_data
from .models import Stock
from fuzzywuzzy import fuzz, process
from django.core.cache import cache
import json

def get_stocks():
    cached_stocks = cache.get('stocks_list')
    if cached_stocks is None:
        stocks = list(Stock.objects.all().values('company_name', 'company_symbol'))
        cached_stocks = [{'name': stock['company_name'], 'symbol': stock['company_symbol']} for stock in stocks]
        cache.set('stocks_list', cached_stocks, timeout=None)  # No timeout for indefinite caching
    return cached_stocks

def index(request):
    return render(request, 'home/index.html')


def stock_db(request , stock_symbol):
    if not stock_symbol:
        return HttpResponse("No stock symbol provided")
    
    stock_symbol = stock_symbol.upper()
    stock = get_object_or_404(Stock, company_symbol=stock_symbol)
    data = get_one_stock_data(stock_symbol)
    if not data:
        return HttpResponse(f"Data for stock symbol {stock_symbol} not found")
    
    del data['ssid']
    del data['date']
    
    with open('data.json', 'w') as f:
        json.dump(data, f)
    data['symbol'] = stock_symbol
    return render(request, 'stocks/stock_details.html', {'stock': data})

def get_stock_suggestions(query, limit=5):
    stocks = get_stocks()
    suggestions = process.extract(query, [stock['name'] for stock in stocks], scorer=fuzz.partial_ratio, limit=limit)
    suggested_stocks = [stock for stock in stocks if any(stock['name'] == suggestion[0] for suggestion in suggestions)]
    return sorted(suggested_stocks, key=lambda x: fuzz.token_sort_ratio(x['name'], query), reverse=True)

def stock_suggestions(request):
    query = request.GET.get('q', '').strip()
    if query:
        suggestions = get_stock_suggestions(query)
        return JsonResponse(suggestions, safe=False)
    return JsonResponse([], safe=False)
