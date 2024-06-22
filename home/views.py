from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from .scraper import Scraper
import json

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
