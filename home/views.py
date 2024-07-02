from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from .scraper import Scraper
import json

from .insert_db import get_list_of_stocks,get_one_stock_data

# Create your views here.

def index(request):

    # Page from the theme 
    return render(request, 'pages/index.html')



def stock(request, stock_symbol):
    return HttpResponse(f"Stock symbol: {stock_symbol}")


def stock_scrape(request , stock_symbol):
    if not stock_symbol:
        return HttpResponse("No stock symbol provided")
    scraper = Scraper()
    data = scraper.scrape(
        stock_name=stock_symbol,
        save_to_db=False
    )
    data['symbol'] = stock_symbol
    return render(request, 'stocks/stock_details.html', {'stock': data})



def stick_scrape_json(request , stock_symbol):
    if not stock_symbol:
        return HttpResponse("No stock symbol provided")
    scraper = Scraper()
    data = scraper.scrape(
        stock_name=stock_symbol,
        save_to_db=False
    )
    data['symbol'] = stock_symbol
    return JsonResponse(data)
    
def stock_admin_update(request):

    stocks = get_list_of_stocks()
    for stock in stocks:
        scraper = Scraper()
        data = scraper.scrape(
            stock_name=stock,
            save_to_db=True
        )
    return JsonResponse({'message': 'Stocks updated successfully'})
    

def stock_db(request , stock_symbol):
    if not stock_symbol:
        return HttpResponse("No stock symbol provided")

    data = get_one_stock_data(stock_symbol)
    print(data)
    del data['ssid']
    del data['date']
    with open('data.json', 'w') as f:
        json.dump(data, f)


    


    data['symbol'] = stock_symbol
    return render(request, 'stocks/stock_details.html', {'stock': data})


from django.http import JsonResponse
from fuzzywuzzy import fuzz, process

def load_stocks_from_file(filename):
    stocks = []
    with open(filename, 'r') as file:
        for line in file:
            name, symbol = line.strip().split(',')
            stocks.append({"name": name, "symbol": symbol})
    return stocks

# Assuming 'stocks.txt' is in the same directory as your script
stocks = load_stocks_from_file('./stock_data.txt')

def get_stock_suggestions(query, limit=5):
    suggestions = process.extract(query, [stock['name'] for stock in stocks], scorer=fuzz.partial_ratio, limit=limit)
    suggested_stocks = [stock for stock in stocks if any(stock['name'] == suggestion[0] for suggestion in suggestions)]
    return sorted(suggested_stocks, key=lambda x: fuzz.token_sort_ratio(x['name'], query), reverse=True)

def stock_suggestions(request):
    query = request.GET.get('q', '').strip()
    if query:
        suggestions = get_stock_suggestions(query)
        return JsonResponse(suggestions, safe=False)
    return JsonResponse([], safe=False)
