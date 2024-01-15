import MetaTrader5 as mt
from datetime import datetime


class MyTraderMt5:

    def __init__(self, login, password, server):
        super().__init__()
        self.login = login
        self.password = password
        self.server = server

    def test(self, symbol="BTCUSD"):
        res_init = mt.initialize()
        res_login = mt.login(self.login, self.password, self.server)
        print (res_init)
        print(res_login)
        rates = mt.copy_rates_from(symbol, mt.TIMEFRAME_D1, datetime.now(), 100)
        print (rates)
        account_info = mt.account_info()
        print (account_info)
        print(f"Balance {account_info.balance}")

        symbol_info  = mt.symbols_get(symbol)
        print (symbol_info)
