import time
from datetime import datetime

import MetaTrader5 as mt


# Every trader of this type is connected to a symbol. For default trader new are
# opened on bitcoins
class MyTraderMt5:

    def __init__(self, login, password, server, symbol="BTCUSD"):
        super().__init__()
        self.login = login
        self.password = password
        self.server = server
        self.symbol = symbol
        res_init = mt.initialize()
        res_login = mt.login(self.login, self.password, self.server)
        

    def test_account(self):
        rates = mt.copy_rates_from(self.symbol, mt.TIMEFRAME_D1, datetime.now(), 100)
        print (rates)
        account_info = mt.account_info()
        print (account_info)
        print(f"Balance {account_info.balance}")
        symbols = mt.symbols_get()
        print(f"Total symbols of account: {len(symbols)}")
        symbol_info  = mt.symbols_get(self.symbol)
        print (f"{self.symbol} info detailed: {symbol_info}")
        self.positionAnalysis()
        
    def positionAnalysis(self):
        pos = mt.positions_get(symbol=self.symbol)
        for pos_open in pos:
            sell_pos = pos_open.type == 1
            buy_pos = pos_open.type == 0
            if (sell_pos):
                msg = " sell "
            else:
                msg = " buy "
            if pos_open.profit < 0:
                print (f" Position {pos_open.ticket} opened like {msg} loosing {pos_open.profit}")
            if pos_open.profit > 0:
                print (f" Position {pos_open.ticket} opened like {msg} earning {pos_open.profit}")
    
    def send_order(self, req, n=5):
        for _ in range(n):
            res = mt.order_send(req)
           
            if res is not None and res.retcode == mt.TRADE_RETCODE_DONE:
                break
            else:
                print(req)
                print(res)
                time.sleep(0.5)
        return res
    
    def buyOrder(self, lot, tp= 0, sl=0):
        if tp == 0:
            tp = mt.symbol_info_tick(self.symbol).ask+(mt.symbol_info_tick(self.symbol).ask *0.010)
        if sl == 0:
            sl = mt.symbol_info_tick(self.symbol).ask-(mt.symbol_info_tick(self.symbol).ask *0.010)
        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": lot,
            "type": mt.ORDER_TYPE_BUY,
            "price": mt.symbol_info_tick(self.symbol).ask,
            "tp": tp,
            "sl": sl
        }
        order = self.send_order(request)
        
        return order
        
    def sellOrder(self,  lot, tp=0, sl=0):
        if tp == 0:
            tp = mt.symbol_info_tick(self.symbol).bid-(mt.symbol_info_tick(self.symbol).bid *0.010)
        if sl == 0:
            sl = mt.symbol_info_tick(self.symbol).bid+(mt.symbol_info_tick(self.symbol).bid *0.010)
        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": lot,
            "type": mt.ORDER_TYPE_SELL,
            "price": mt.symbol_info_tick(self.symbol).bid,
            "tp": tp,
            "sl": sl
        }
        order = self.send_order(request)
        return order

    def closeOrderAtMarket(self, ticket):
        mt.Close(self.symbol, ticket = ticket)
        
    def status(self):
        self.test_account(f"TRADER ON {self.symbol}")
        print("__________________________________POSITION ACTUAL_______________________________________")
        self.positionAnalysis()
        print("________________________________________________________________________________________")
        print("________________________________________________________________________________________")
        
    # Testing simple useless strategy: open one buy and one sell order if  position is empty
    def strategyOrder(self):
        rates = mt.copy_rates_from(self.symbol, mt.TIMEFRAME_D1, datetime.now(), 100)
        pos = mt.positions_get(symbol=self.symbol)
        if len(pos) == 0:
            print(self.buyOrder(0.01))
            print(self.sellOrder(0.01))
    # Testing simple trading: close order that are in profit
    def operationTrade(self):
        pos = mt.positions_get(symbol=self.symbol)
        for pos_open in pos:
            sell_pos = pos_open.type == 1
            buy_pos = pos_open.type == 0
            if (sell_pos):
                msg = " sell "
            else:
                msg = " buy "
            if pos_open.profit > 0:
                print (f" Try to close {pos_open} open for {msg}")
                resp = self.closeOrderAtMarket(pos_open.ticket)
                print(resp)