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
                    myt.info_account_and_symbol()
                    iter = 0
                    while True:
                        iter+= 1
                        if iter % 10 == 1:
                            print("Verifica ..:")
                        myt.strategyOrder()
                        myt.operationTrade(0.50)
                        time.sleep(3)

except Exception as e:
    print(e)