import pandas as pd
import yfinance as yf
from datetime import datetime


class Portfolio:
    def __init__(self, initial_cash):
        self.cash = initial_cash
        self.stocks = {}

    def add_stock(self, ticker):
        if ticker not in self.stocks:
            self.stocks[ticker] = Stock(ticker)

    def buy_stock(self, ticker, shares, price):
        self.add_stock(ticker)
        total_cost = shares * price
        if self.cash < total_cost:
            raise ValueError("Not enough cash to buy")
        self.stocks[ticker].buy(shares, price)
        self.cash -= total_cost

    def sell_stock(self, ticker, shares, price):
        if ticker not in self.stocks:
            raise ValueError(f"No holdings in {ticker}")
        revenue = self.stocks[ticker].sell(shares, price)
        self.cash += revenue

    def get_portfolio_value(self):
        total_value = self.cash
        for ticker, stock in self.stocks.items():
            current_price = yf.Ticker(ticker).history(
                period='1d')['Close'].iloc[-1]
            total_value += stock.current_value(current_price)
        return total_value

    def get_stock_info(self, ticker):
        if ticker not in self.stocks:
            return None
        stock = self.stocks[ticker]
        current_price = yf.Ticker(ticker).history(
            period='1d')['Close'].iloc[-1]
        return {
            'Ticker': ticker,
            'Shares': stock.shares,
            'Average Cost': stock.average_cost(),
            'Current Price': current_price,
            'Current Value': stock.current_value(current_price)
        }

    def print_portfolio(self):
        print(f"Cash: ${self.cash:.2f}")
        for ticker, stock in self.stocks.items():
            info = self.get_stock_info(ticker)
            if info:
                print(f"{info['Ticker']}: {info['Shares']} shares, Average Cost: ${info['Average Cost']:.2f}, Current Price: ${info['Current Price']:.2f}, Current Value: ${info['Current Value']:.2f}")
        print(f"Total Portfolio Value: ${self.get_portfolio_value():.2f}")
