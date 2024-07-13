from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Stock
from .scraper import Scraper

class StockBulkAddForm(forms.Form):
    data = forms.CharField(widget=forms.Textarea, help_text="Enter company name and symbol, separated by a comma, one pair per line.")


class StockAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_symbol')
    search_fields = ('company_name', 'company_symbol')

    def get_urls(self):
        urls = super().get_urls()
        print(urls)
        custom_urls = [
            path('bulk-add/', self.admin_site.admin_view(self.bulk_add_view), name='bulk_add_stocks'),
            path('update-stocks/', self.admin_site.admin_view(self.stock_admin_update), name='stock_admin_update'),
        ]
        return custom_urls + urls
    def bulk_add_view(self, request):
        if request.method == 'POST':
            form = StockBulkAddForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data['data']
                lines = data.split('\n')
                created_stocks = []
                for line in lines:
                    try:
                        company_name, company_symbol = map(str.strip, line.split(','))
                        stock, created = Stock.objects.get_or_create(company_name=company_name, company_symbol=company_symbol)
                        if created:
                            created_stocks.append(stock)
                    except ValueError:
                        messages.error(request, f"Invalid format for line: {line}")
                if created_stocks:
                    messages.success(request, f"Successfully added {len(created_stocks)} stocks.")
                return redirect('admin:home')  # Redirect to stock change list
        else:
            form = StockBulkAddForm()
        context = {
            'form': form,
            'title': 'Bulk Add Stocks',
            'app_label': self.model._meta.app_label,
        }
        return render(request, 'admin/stock_bulk_add.html', context)
    
    def stock_admin_update(self, request):
        stocks = Stock.objects.all().values('company_symbol')
        for stock in stocks:
            print(f"Updating stock: {stock['company_symbol']}")
            try:
                scraper = Scraper()
                stock = stock['company_symbol'].upper()
                data = scraper.scrape(
                    stock_name = stock,
                    save_to_db=True
                )
            except Exception as e:
                print(f"Error: {e}")
                messages.error(request, f"Error updating stock: {stock}")
                continue
        messages.success(request, 'Stocks updated successfully')
        return redirect('admin')
    
admin.site.register(Stock, StockAdmin)