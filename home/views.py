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
