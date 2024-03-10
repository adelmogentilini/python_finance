from simulator import Simulator
from simulator import StrategyTrade
import yaml

if __name__ == '__main__':
    # symbol_lists = ['EURUSD=X', 'CL=F', 'FTSEMIB.MI']
    # symbol_lists = ['BTC-EUR', 'EURUSD=X']
    try:
        with open("config/config.yaml", 'r') as file:
            properties = yaml.load(file, Loader=yaml.SafeLoader)
            symbol_lists = properties.get('symbol_lists')
    except Exception as e:
        print('FILE DI CONFIG non trovato o incompleto => utilizzo i parametri di default')
    StrategyTrade
    bearish_bullish = StrategyTrade()
    Simulator
    sim = Simulator()
    all_strategy = [bearish_bullish]
    for order_index in range(0, len(all_strategy)):
        StrategyTrade
        strategy = all_strategy[order_index]
        sim.simulation(strategy, symbol_lists)
        tot = 0
        sim.resultsSimulation(strategy, symbol_lists, False)