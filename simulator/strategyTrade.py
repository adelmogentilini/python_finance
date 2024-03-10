"""
Every strategy must define:
    signal_generator: function for signal generator that put order when is needed
    stop_loss, take_profit: function for calculate stop_loss and take_profit relative at this strategy
    pric: function for determine price of the asset in a date moment
"""
class StrategyTrade:
    def __init__(self):
        super().__init__()
        self.take_profit = None
        self.stop_loss = None
        self.orders = []

    def description(self):
        return """
            Simple strategy used for example start point with analyze candle stick for identify bullish and bearish pattern
        """
    # core of simulation models: decide if the pattern examined is a pattern tha indicate to buy or to sell or  do
    # nothing
    def signal_generator(self, df_ext, index, symbol):
        df = df_ext[index - 1:index + 1]
        open_quot = df.open.iloc[-1]
        close = df.close.iloc[-1]
        previous_open = df.open.iloc[-2]
        previous_close = df.close.iloc[-2]
        actual_quote = df_ext[index + 1:index + 2]
        if open_quot > close and close < previous_open < previous_close <= open_quot:
            # bearish: verde seguita da rossa piu grande => ribassista => sell
            self.orders.append(["SELL", actual_quote.open.iloc[-1], symbol])
            return 1
        elif (open_quot < close and
              close > previous_open > previous_close >= open_quot):
            # bullish: rossa seguita da verde piu grande => rialzista => buy
            self.orders.append(["BUY", actual_quote.open.iloc[-1], symbol])
            return 2
        else:
            return 0

    def stopLoss(self):
        if self.stop_loss is None:
            self.stop_loss = 15
        return self.stop_loss
    
    def takeProfit(self):
        if self.take_profit is None:
            self.take_profit = 8
        return self.take_profit

    def price(self, df, index):
        return df[index + 1:index + 2].open.iloc[-1]