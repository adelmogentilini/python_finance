import yaml

from mt5.myTraderMt5 import MyTraderMt5

demo_mode = True

try:
    with open("config_trade.yaml", 'r') as file:
        properties = yaml.load(file, Loader=yaml.SafeLoader)
        conti = properties.get('conti')
        print (conti)
        for k in conti:
            if demo_mode:
                if k.get('nome') == "demo":
                    myt = MyTraderMt5(k.get('login'), k.get('password'), k.get('server'))
                    myt.test()



except Exception as e:
    print('FILE DI CONFIG non trovato o incompleto ')