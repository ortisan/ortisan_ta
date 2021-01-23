# coding=utf-8
__author__ = 'Marcelo Ortiz'

from datetime import datetime
import rx

class MarketSimulator(object):
    """
    Simulator for backtesting
    """
    brokerage = 0
    init_amount = 0.0
    current_amount = 0.0

    def __init__(self, init_amount, brokerage=20):
        self.init_amount = init_amount
        self.current_amount = init_amount
        self.brokerage = brokerage

    def evaluate(self, symbol: str, price: float):
        """
        Evaluate if hits stops. If yes, buy or sell. Else ajusts stops

        Keyword arguments:
        symbol -- Código do ativo
        price -- Preço atual
        """
        operations = None

        if not symbol in self.symbols_operations:
            return
        if symbol in self.symbols_operations:
            operations = self.symbols_operations[symbol]
        else:
            operations = []

        operations_mached = [operation for operation in operations if
                             price <= operation.stop_loss or price >= operation.stop_gain]

        self.sell(symbol, price, operations_mached)
        self.__adjust_stops(symbol, new_price=price)



    def buy(self, date: datetime, symbol: str, quantity: int, price: float, stop_loss: float, stop_gain: float):
        """
        Buy simulation
        Keyword arguments:
        date -- Operation's date
        symbol -- Asset symbol
        quantity -- Amount
        stop_loss -- Stop loss
        stop_gain -- Stop gain
        """

        operations = []
        if symbol in self.symbols_operations:
            operations = self.symbols_operations[symbol]
        total_price = quantity * price - self.brokerage
        if total_price <= self.current_amount:
            self.current_amount = self.current_amount - total_price
            operation = OperationItem(quantity, price, stop_loss, stop_gain)
            operations.append(operation)
            self.symbols_operations[symbol] = operations
        else:
            print('does not have money')

    def sell(self, date: datetime, symbol: str, price: float, operations: list):
        """
        Sell simulation
        Keyword arguments:
        date -- Operation's date
        symbol - Asset symbol
        price - Price now
        operations - History of operations
        """
        for operation in operations:
            quantity = operation.quantity
            total_price = quantity * price - self.brokerage
            self.current_amount = self.current_amount + total_price
            self.symbols_operations[symbol].remove(operation)

    def sell_all(self, symbol: str, price: float):
        operations = []
        if symbol in self.symbols_operations:
            operations = self.symbols_operations[symbol]
        if len(operations) > 0:
            self.sell(symbol, price=price, operations=operations)

    def get_percent_gain(self):
        return self.current_amount / self.init_amount - 1

    def get_gain(self):
        return self.current_amount - self.init_amount

    def __adjust_stops(self, symbol: str, new_price: float):
        """
        Ajust stop loss according price changes

        Keyword arguments:
        symbol - Asset code
        new_price - new price
        """
        operations = self.symbols_operations[symbol]
        for operation in operations:
            price = operation.price
            perc_of_gain = (new_price / price) - 1
            if perc_of_gain > 0:
                operation.stop_loss = operation.stop_loss + operation.stop_loss * perc_of_gain


class OperationItem(object):
    date = None
    quantity = 0
    price = 0.0
    stop_loss = 0.0
    stop_gain = 0.0

    def __init__(self, date: datetime, quantity: int, price: float, stop_loss: float, stop_gain: float):
        self.date = date
        self.quantity = quantity
        self.price = price
        self.stop_loss = stop_loss
        self.stop_gain = stop_gain
