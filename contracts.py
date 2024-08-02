from abc import ABC, abstractmethod
from typing import Literal
from datetime import datetime

class Contract(ABC):
    def __init__(self, currency: Literal['BTC'], expiry: str, size: float, timestamp: int, avg_open: float):
        self.currency = currency # ^^^ more currencies can be added later.      NOTE: ^^^ need to figure out the right way to deal w/ different time data.
        self.expiry = self.parse_expiry(expiry)
        self.size = size
        self.timestamp = timestamp
        self.avg_open = avg_open
        self.mark_price = avg_open

    def parse_expiry(self, expiry: str) -> datetime:
        try:
            return datetime.strptime(expiry, "%d-%b-%y")
        except ValueError:
            raise ValueError("Expiry date must be in format 'DD-MM-YY")
    
    @abstractmethod
    def get_greeks(self, *params):
        pass
    
    @abstractmethod
    def update(self, *params):
        pass



class Future(Contract):
    def __init__(self, currency, expiry, size, timestamp, avg_open, mark_price):
        super().__init__(currency, expiry, size, timestamp, avg_open, mark_price)

    
    def get_basis(self, spot_mark, future_mark):
        return future_mark - spot_mark
    
    def get_greeks(self):
        delta = 1 * self.size
        return {
            'delta': delta
        }


class Option(Contract):
    def __init__(self, currency, expiry, strike: int, type: Literal['call', 'put'], size, timestamp, avg_open, mark_price):
        super().__init__(currency, expiry, size, timestamp, avg_open, mark_price)
        
        self.type = type
        self.strike = strike

    def get_greeks(self, time_now, spot_price, strike_price, volatility, risk_free_rate):
        S = spot_price
        K = self.strike
        T = self.expiry - time_now
        v = volatility
        r = risk_free_rate

        delta = 0
        gamma = 0
        vega = 0
        theta = 0
        rho = 0

        return {
            'delta': delta,
            'gamma': gamma,
            'vega': vega,
            'theta': theta,
            'rho': rho
        }



class Engine():
    def __init__(self, time, unit_of_time, running_data):
        self.time = time
        self.unit_of_time = unit_of_time
    
    def update(self):
        self.time += self.unit_of_time

    