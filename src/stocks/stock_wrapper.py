from bd3.src.stocks.btc.btc_wrapper import get
from bd3.src.stocks.tsla.tsla_wrapper import get


class Wrapper:
    
    def __init__(self):
        self.data = self.StockData()

    def get(self):
        return self.data

    def save(self):
        self.data.btc.to_csv("btc.csv")
        self.data.tsla.to_csv("tsla.csv")
  
    class StockData:
        def __init__(self):
            self.btc = get()
            self.tsla = get()
             
