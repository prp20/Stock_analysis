import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from time import sleep
from pymongo import MongoClient

mongo_uri = "mongodb://localhost:27017/"


def get_number_from_percentage(li):
    num_span = li.find('span', {'class': 'number'})
    num_span = num_span.text.replace(',', '')
    return float(num_span) if (num_span != '') else 0.0


def get_company_fundamentals(SCRIP):
    link = f'https://www.screener.in/company/{SCRIP}/consolidated'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(link, headers=hdr)

    try:
        page = urlopen(req)
        soup = BeautifulSoup(page)

        div_html = soup.find('div', {'class': 'company-ratios'})
        ul_html = div_html.find('ul', {'id': 'top-ratios'})
        company_val = {}
        for li in ul_html.find_all("li"):
            name_span = li.find('span', {'class': 'name'})
            company_val['ticker'] = SCRIP
            if 'Market Cap' in name_span.text:
                company_val['Market Cap'] = round(
                    get_number_from_percentage(li), 2)
            elif 'Stock P/E' in name_span.text:
                company_val['P/E'] = round(get_number_from_percentage(li), 2)
            elif 'ROCE' in name_span.text:
                company_val['ROCE'] = round(get_number_from_percentage(li), 2)
            elif 'ROE' in name_span.text:
                company_val['ROE'] = round(get_number_from_percentage(li), 2)
            elif 'Book Value' in name_span.text:
                company_val['Book Value'] = round(
                    get_number_from_percentage(li), 2)
            elif 'Current Price' in name_span.text:
                company_val['Price'] = round(get_number_from_percentage(li), 2)
        print(f'MARKET CAPITILIZATION - {SCRIP}: {company_val} Cr')

    except:
        print(f'EXCEPTION THROWN: UNABLE TO FETCH DATA FOR {SCRIP}')
        company_val = {}
    return company_val


def load_data():
    new_data = pd.read_csv('ratio_nifty100.csv')
    new_data.dropna(how='all', axis=1, inplace=True)
    new_data.drop(columns=new_data.columns[0], axis=1,  inplace=True)
    return new_data


def get_number_from_percentage(li):
    num_span = li.find('span', {'class': 'number'})
    num_span = num_span.text.replace(',', '')
    return float(num_span) if (num_span != '') else 0.0


def get_cols(html_val):
    cols = ['Columns Name']
    col_name = html_val.find("table").find("thead").find_all("tr")
    val_list = col_name[0].get_text().split("\n")
    for val in val_list:
        if val != "":
            cols.append(val.split("  ")[-1]
                        ) if val.split("  ")[-1] != "" else None
    return cols


def get_dataframe_from_table(div_html, cols, dataframe):
    col_name = div_html.find("table").find("tbody").find_all("tr")
    rows = div_html.find("table").find("tbody").find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        data = {}
        row_head = cells[0].get_text().split("\n")
        if len(row_head) > 1:
            data[cols[0]] = cells[0].get_text().split("\n")[2]
        else:
            data[cols[0]] = cells[0].get_text().split("\n")[0]
        for idx, col in enumerate(cols[1:]):
            text_val = cells[idx+1].get_text().split("\n")
            if text_val[0]:
                if "%" not in text_val[0] and "\n" not in text_val[0]:
                    text_val[0] = float(text_val[0].replace(",", ""))
                else:
                    text_val[0] = float(text_val[0].replace("%", ""))
            data[col] = text_val[0]
        dataframe = pd.concat(
            [dataframe, pd.DataFrame([data])], ignore_index=True)
    return dataframe


def load_page(link):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(link, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features='lxml')
    return soup


def insert_df_to_db(db_name, collection_name, data):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    data_dict = data.to_dict("records")
    collection.insert_many(data_dict)
    print("Data inserted successfully")
    client.close()

def update_or_insert_to_db(db_name, collection_name, data):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    data_dict = data.to_dict("records")
    collection.insert_many(data_dict)
    print("Data inserted successfully")
    client.close()