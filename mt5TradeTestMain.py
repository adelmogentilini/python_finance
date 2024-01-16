import time

import yaml

from mt5 import MyTraderMt5

demo_mode = True
symbol = "BTCUSD"
try:
    with open("config/config_trade.yaml", 'r') as file:
        properties = yaml.load(file, Loader=yaml.SafeLoader)
        conti = properties.get('conti')
        print (conti)
        for k in conti:
            if demo_mode:
                if k.get('nome') == "demo":
                    myt = MyTraderMt5(k.get('login'), k.get('password'), k.get('server'))
                    #myt.test(symbol)
                   
                    while True:
                        print("Verifica ..:")
                        myt.strategyOrder()
                        myt.operationTrade()
                        time.sleep(3)

except Exception as e:
    print(e)