import psycopg2
from psycopg2 import sql


db_params = {
    'dbname': 'stocks',
    'user': 'postgres',
    'password': '163538',
    'host': 'localhost',  
    'port': '5432'  
}

import os
import pandas as pd

from datetime import datetime

import json


def create_or_update_stock(stock_name, ssid, data_dict):
    current_date = datetime.now()
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        create_table_query = '''
        CREATE TABLE IF NOT EXISTS stocks_data (
            ssid VARCHAR,
            stock_name VARCHAR UNIQUE,
            date TIMESTAMP,
            PRIMARY KEY (stock_name)
        );
        '''
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'stocks_data' created successfully")

        for column_name, data_list in data_dict.items():

            add_column_query = sql.SQL('''
            ALTER TABLE stocks_data
            ADD COLUMN IF NOT EXISTS {column} JSONB;
            ''').format(column=sql.Identifier(column_name))
            cursor.execute(add_column_query)
            connection.commit()
            print(f"Column '{column_name}' added to table 'stocks_data'")


            cursor.execute(sql.SQL('''
            INSERT INTO stocks_data (ssid, stock_name, date, {column})
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (stock_name)
            DO UPDATE SET {column} = EXCLUDED.{column}, ssid = EXCLUDED.ssid, date = EXCLUDED.date;
            ''').format(column=sql.Identifier(column_name)),
            [ssid, stock_name, current_date, json.dumps(data_list)])
            connection.commit()
            print(f"Data for '{column_name}' inserted/updated for stock '{stock_name}'")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")