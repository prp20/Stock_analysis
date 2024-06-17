import streamlit as st
import time
import pandas as pd
import yfinance as yf
import numpy as np
import requests
from time import sleep
import datetime as dt
import plotly.express as px
from fastapi import FastAPI, Response
import time
import utils
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from time import sleep


class FundamentalAnalysis:
    def __init__(self, ticker):
        self.ticker = ticker

    def get_quaterly_results(self):
        link = f"https://www.screener.in/company/{self.ticker}/consolidated/"
        soup = utils.load_page(link)
        div_html = soup.find('section', {'id': 'quarters'})
        cols = utils.get_cols(div_html)
        quaterly_sheet = pd.DataFrame(columns=cols)
        quaterly_sheet = utils.get_dataframe_from_table(
            div_html, cols, quaterly_sheet)
        return quaterly_sheet

    def get_pandl_data(self):
        link = f"https://www.screener.in/company/{self.ticker}/consolidated/"
        soup = utils.load_page(link)
        div_html = soup.find('section', {'id': 'profit-loss'})
        cols = utils.get_cols(div_html)
        pandl_sheet = pd.DataFrame(columns=cols)
        pandl_sheet = utils.get_dataframe_from_table(
            div_html, cols, pandl_sheet)
        return pandl_sheet

    def get_balance_sheet_data(self):
        link = f"https://www.screener.in/company/{self.ticker}/consolidated/"
        soup = utils.load_page(link)
        div_html = soup.find('section', {'id': 'balance-sheet'})
        cols = utils.get_cols(div_html)
        balance_sheet = pd.DataFrame(columns=cols)
        balance_sheet = utils.get_dataframe_from_table(
            div_html, cols, balance_sheet)
        return balance_sheet


def main():
    stock_fa = FundamentalAnalysis("INFY")
    print(stock_fa.get_balance_sheet_data())
    print(stock_fa.get_pandl_data())
    print(stock_fa.get_quaterly_results())
    # fund_df = pd.concat([balance_sheet, pandl_sheet], ignore_index=True)
    # print(fund_df)


if __name__ == "__main__":
    main()
