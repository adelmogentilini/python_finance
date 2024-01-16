import datetime

import pandas as pd
import yfinance as yf


class Simulator:

    def __init__(self):
        super().__init__()
        self.results = []

    def checkOrderTPSL(self, strategy, quot):
        for order_index in range(0, len(strategy.orders)):
            order = strategy.orders[order_index]
            if order[0] == 'BUY':
                max_loss = order[1] - strategy.stopLoss()
                max_profit = order[1] + strategy.takeProfit()
                if quot >= max_profit:
                    order[0] = 'CLOSED +'
                    order[1] = quot - order[1]
                if quot <= max_loss:
                    order[0] = 'CLOSED -'
                    order[1] = quot - order[1]
            elif order[0] == 'SELL':
                max_loss = order[1] + strategy.stopLoss()
                max_profit = order[1] - strategy.takeProfit()
                if quot <= max_profit:
                    order[0] = 'CLOSED +'
                    order[1] = order[1] - quot
                if quot >= max_loss:
                    order[0] = 'CLOSED -'
                    order[1] = order[1] - quot

    # simulation, for default is on 59 days with 15 minutes of interval
    # on yahoo finance 60 days is max for 15 min of interval
    def simulation(self, strategy, symbol_lists_par, day=59, interval="15m"):
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=day)
        print(f" Analysis from {start_date} to {end_date} on {symbol_lists_par}")
        if len(symbol_lists_par) > 1:
            df = yf.download(tickers=symbol_lists_par, start=start_date, end=end_date, interval=interval).stack()
            df.columns = df.columns.str.lower()
            df.index.names = ['date', 'ticker']
            grouped = df.groupby(level=1)
            for key, group in grouped:
                print(f"Tick key {key}:")
                self.singleDfSimulation(group, strategy, key)
        else:
            df = yf.download(tickers=symbol_lists_par, start=start_date, end=end_date, interval="15m")
            df.columns = df.columns.str.lower()
            self.singleDfSimulation(df, strategy, symbol_lists_par[0])

    def singleDfSimulation(self, df, strategy, symbol):
        signal = [0]
        last_price = strategy.price(df, 1)
        for i in range(1, len(df) - 1):
            send_buy = strategy.signal_generator(df, i, symbol)
            signal.append(send_buy)
            # Order and check are did for default on  next OPEN
            # if signal is not 0 I did an order, if some order is in TP or in SL
            # calculate PROFIT ad close order
            self.checkOrderTPSL(strategy, strategy.price(df, i))
            last_price = strategy.price(df, i)
        signal.append(-1)  # append last value useless signal
        df["SIGNAL"] = signal

        self.results.append((symbol, last_price, df.SIGNAL.value_counts().drop([0,-1])))

    def resultsSimulation(self, strategy, symbol_lists_par, print_order=False):
        tot = 0
        tot_pending = 0
        num_valid = 0
        num_tot = 0
        if print_order:
            print(strategy.orders)
        for order_index in range(0, len(strategy.orders)):
            num_tot += 1
            if strategy.orders[order_index][0] not in ("BUY", "SEND"):
                num_valid += 1
                tot = tot + strategy.orders[order_index][1]
            else:
                tot_pending = tot_pending + strategy.orders[order_index][1] - self.get_last_price(strategy.orders[order_index][2])

        print(strategy.description())
        print(self.results)
        print(f"total order closed {num_valid} on {num_tot}, already open {num_tot - num_valid}, trade with 1 stock  unit on  {symbol_lists_par} earned {tot}")
        print(f"closing {num_tot - num_valid} pending earned: {tot_pending} so real earn: {tot + tot_pending}")

    def get_last_price(self, symbol):
        for index in range(0, len(self.results)):
            if self.results[index][0] == symbol:
                return self.results[index][1]