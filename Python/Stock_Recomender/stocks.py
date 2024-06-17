import pandas as pd
import yfinance as yf
from datetime import datetime


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.shares = 0
        self.cost_basis = 0.0
        self.transactions = []

    def buy(self, shares, price):
        total_cost = shares * price
        self.shares += shares
        self.cost_basis += total_cost
        self.transactions.append(
            {'type': 'buy', 'shares': shares, 'price': price, 'date': datetime.now()})
        print(f"Bought {shares} shares of {self.ticker} at {price}")

    def sell(self, shares, price):
        if shares > self.shares:
            raise ValueError("Not enough shares to sell")
        total_revenue = shares * price
        self.shares -= shares
        # Adjust cost basis
        self.cost_basis -= (self.cost_basis / (self.shares + shares)) * shares
        self.transactions.append(
            {'type': 'sell', 'shares': shares, 'price': price, 'date': datetime.now()})
        print(f"Sold {shares} shares of {self.ticker} at {price}")
        return total_revenue

    def current_value(self, current_price):
        return self.shares * current_price

    def average_cost(self):
        return self.cost_basis / self.shares if self.shares else 0
