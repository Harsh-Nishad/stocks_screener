import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import os

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

from .initial import HEADERS1, get_soup, GRAPH_PARMS, HEADERS2, get_hash
from .insert_db import create_or_update_stock

class Scraper:

    def __init__(self):
        pass

    def clean_keys(self, data):
        new_data = {}
        for key in data.keys():
            new_key = key.strip().replace(' ', '_').lower()
            # change . to _ in keys
            new_key = new_key.replace('.', '_')
            # replace __ with _ and remove _ if at the end or start
            new_key = new_key.replace('__', '_').strip('_')
            # remove % from keys
            new_key = new_key.replace('%', 'percent')
            # change / to _ in keys
            new_key = new_key.replace('/', '_')
            new_data[new_key] = data[key]
        return new_data

    def start_scraping(self, save_to_db=True):
        try:
            print("Reading stock list")
            with open('stock_list.txt', 'r') as file:
                stock_list = file.readlines()
                for stock in stock_list:
                    print(f"Scraping data for {stock}")
                    stock = stock.strip()
                    url = f'https://www.screener.in/company/{stock}/consolidated/'
                    self.url = url
                    data = self.scrape(stock, save_to_db)
                    if not save_to_db:
                        print(json.dumps(data, indent=4))  # Print the data if not saving to DB
                    return data



        except Exception as e:
            print(f"Error: {e} in start scraping def")
            return None

    def scrape(self, stock_name, save_to_db=True):
        self.stock_name = stock_name
        self.url = f'https://www.screener.in/company/{stock_name}/consolidated/'
        tabluar_data = {}
        ssid = get_hash(stock_name)
        soup = get_soup(self.url, HEADERS1)
        tabluar_data['balance_sheet'] = json.loads(self.get_balance_sheet(soup))
        tabluar_data['cash_flow'] = json.loads(self.get_cash_flow(soup))
        tabluar_data['ratios'] = json.loads(self.get_ratios(soup))
        tabluar_data['quarters'] = json.loads(self.get_quarters(soup))
        tabluar_data['profit_loss'] = json.loads(self.get_profit_loss(soup))
        tabluar_data['shareholding_qtr'] = json.loads(self.get_shareholding_qtr(soup))
        tabluar_data['shareholding_annual'] = json.loads(self.get_shareholding_annual(soup))
        # tabluar_data['peers'] = json.loads(self.get_peers_data(soup))
        tabluar_data['peers'] = [ self.clean_keys(peer_data) for peer_data in json.loads(self.get_peers_data(soup)) ]
        tabluar_data['company_ratios'] = self.clean_keys(self.get_company_ratios(soup))
        tabluar_data['company_documents'] = self.get_company_documents(soup)

        list_of_graphs_tables = self.get_graph_data(soup)

        # tabluar_data.update(list_of_graphs_tables)

        tabluar_data['graph_data'] = list_of_graphs_tables
        tabluar_data['stock_details'] = self.stock_details(soup)


        for key, _list in tabluar_data.items():
            if type(_list) == list:
                # converts dictionaries inside this list to tuple
                new_list = [tuple(d.items()) for d in _list]
                tabluar_data[key] = new_list
            





        with open('./tabluar_data.json', 'w') as file:
            json.dump(tabluar_data, file)

        print("Got all data")
        if save_to_db:
            print("Inserting data into database")
            create_or_update_stock(stock_name, ssid, tabluar_data)
        else:
            return tabluar_data

    def get_balance_sheet(self, soup):
        try:
            balance_sheet = soup.find('section', {'id': 'balance-sheet'})
            table = balance_sheet.find('table', {'class': 'data-table'})
            df = pd.read_html(str(table))[0]
            print("Got balance sheet data")
            return df.to_json(orient='records')
        except Exception as e:
            print(f"Error: {e} in balance sheet def")
            return None

    def get_cash_flow(self, soup):
        try:
            cash_flow = soup.find('section', {'id': 'cash-flow'})
            table = cash_flow.find('table', {'class': 'data-table'})
            df = pd.read_html(str(table))[0]
            print("Got cash flow data")
            return df.to_json(orient='records')
        except Exception as e:
            print(f"Error: {e} in cash flow def")
            return None

    def get_ratios(self, soup):
        try:
            ratios = soup.find('section', {'id': 'ratios'})
            table = ratios.find('table', {'class': 'data-table'})
            df = pd.read_html(str(table))[0]
            print("Got ratios data")
            return df.to_json(orient='records')
        except Exception as e:
            print(f"Error: {e} in ratios def")
            return None

    def get_quarters(self, soup):
        try:
            quarters = soup.find('section', {'id': 'quarters'})
            table = quarters.find('table', {'class': 'data-table'})
            df = pd.read_html(str(table))[0]
            print("Got quarters data")
            data = df.to_json(orient='records')
            return data
        except Exception as e:
            print(f"Error: {e} in quarters def")
            return None

    def get_profit_loss(self, soup):
        try:
            profit_loss = soup.find('section', {'id': 'profit-loss'})
            table = profit_loss.find('table', {'class': 'data-table'})
            df = pd.read_html(str(table))[0]
            print("Got profit loss data")
            return df.to_json(orient='records')
        except Exception as e:
            print(f"Error: {e} in profit loss def")
            return None

    def get_shareholding_qtr(self, soup):
        try:
            shareholding = soup.find('section', {'id': 'shareholding'})
            shareholding_qtr = shareholding.find('div', {'id': 'quarterly-shp'})
            table_shareholding = shareholding_qtr.find('table', {'class': 'data-table'})
            df_shareholding = pd.read_html(str(table_shareholding))[0]
            print("Got shareholding qtr data")
            return df_shareholding.to_json(orient='records')
        except Exception as e:
            print(f"Error: {e} in shareholding def")
            return None

    def get_shareholding_annual(self, soup):
        try:
            shareholding = soup.find('section', {'id': 'shareholding'})
            shareholding_annual = shareholding.find('div', {'id': 'yearly-shp'})
            table_shareholding = shareholding_annual.find('table', {'class': 'data-table'})
            df_shareholding = pd.read_html(str(table_shareholding))[0]
            print("Got shareholding annual data")
            return df_shareholding.to_json(orient='records')
        except Exception as e:
            print(f"Error: {e} in shareholding def")
            return None

    def get_ids(self, soup):
        try:
            company_info = soup.find('div', {'id': 'company-info'})
            company_id = company_info['data-company-id']
            warehouse_id = company_info['data-warehouse-id']
            return warehouse_id, company_id
        except Exception as e:
            print(f"Error: {e} in warehouse id def")
            return None

    def get_peers_data(self, soup):
        try:
            warehouse_id, company_id = self.get_ids(soup)
            print(warehouse_id, company_id)

            url = f'https://www.screener.in/api/company/{company_id}/peers/'
            response = requests.get(url, headers=HEADERS2)

            soup2 = BeautifulSoup(response.text, 'html.parser')

            table_peers = soup2.find('table', {'class': 'data-table'})
            df_peers = pd.read_html(str(table_peers))[0]
            print("Got peers data")
            return df_peers.to_json(orient='records')
        except Exception as e:
            print(f"Error: {e} in peers def")
            return None

    def get_graph_data(self, soup):
        warehouse_id, company_id = self.get_ids(soup)

        url = f'https://www.screener.in/api/company/{company_id}/chart/'
        response = requests.get(url, params=GRAPH_PARMS, headers=HEADERS1)

        if response.status_code != 200:
            print(f"Failed to fetch data for company {company_id}. Status code: {response.status_code}")
            return None

        json_data = response.json()
        datasets = json_data.get("datasets", [])

        if not datasets:
            print(f"No datasets found for company {company_id}")
            return None

        json_data_dict = {}

        for graph in datasets:
            metric = graph["metric"]
            values = graph["values"]

            try:
                df = pd.DataFrame(values, columns=['Date', 'Value'])
                json_data_obj = df.to_dict(orient='records')

                json_data_dict[metric] = json_data_obj
            except Exception as e:
                df = pd.DataFrame(values, columns=['Date', 'Value', 'volume'])
                json_data_obj = df.to_dict(orient='records')

                for i in range(len(json_data_obj)):
                    json_data_obj[i].pop('volume')

                json_data_dict[metric] = json_data_obj
                continue

        print("Got graph data")
        return json_data_dict
    
    def get_company_ratios(self,soup):
        try:
            
            li_elements = soup.select('ul#top-ratios li')

            data_dict = {}
            for li in li_elements:
                key = li.select_one('.name').text.strip()
                number_part = li.select_one('.number').text.strip()
                text_part = li.select_one('.nowrap.value').text.replace(number_part, '').strip()
                
    
                text_part = text_part.replace('\u20b9', '₹').strip()
                value = f"{number_part} {text_part}".strip()
                
                data_dict[key] = value

            #more cleaning
            for key, value in data_dict.items():

            
                value = value.replace('\n', '').strip()
                value = value.replace('Cr.', '').strip()
                value = value.replace(' %', '%').strip()
                value = value.replace(' ', '').strip()
                value = value.replace('\u20b9', '').strip()
                
                data_dict[key] = value

            return data_dict
        except Exception as e:
            print(f"error {e} in get_company_ratios")
            return None
                    


    def get_company_documents(self,soup):
        try:
            documents = soup.find('section', {'id': 'documents'})

            divs = documents.find_all('div', {'class': 'documents'})

            data_documents = {}
            for div in divs:
                key = div.find('h3').text
                links = div.find_all('a')
                data_documents[key] = [link['href'] for link in links]

            return data_documents
        except Exception as e:
            print(f"error {e} in get_company_documents")
            return None
        
    def stock_details(self,soup):
        try:
            div = soup.find('div', class_='company-links')
            data = {}
            for a in div.find_all('a'):
                data[a.text] = a['href']
            data = {k.strip().replace('\n', '').replace('  ', ' '): v.strip().replace('\n', '').replace('  ', ' ') for k, v in data.items()}
            h1 = soup.find('h1', class_='margin-0 show-from-tablet-landscape')
            data['company_name'] = h1.text
            final_data = {}
            for key, value in data.items():
                if 'BSE' in key:
                    bse_id = key.split(' ')[-1]
                    final_data['bse_id'] = bse_id
                    final_data['bse_url'] = value
                elif 'NSE' in key:
                    nse_id = key.split(' ')[-1]
                    final_data['nse_id'] = nse_id
                    final_data['nse_url'] = value
                elif '.com' in key or '.in' in key:
                    final_data['website'] = value
                else:
                    final_data[key] = value
            return final_data

        except Exception as e:
            print("Error in stock_details", e)
            return {}
