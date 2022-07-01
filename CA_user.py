import time
import CA_gas
import os

gas = CA_gas.gas_money()

while True:
    gas.read_gas_prices()
    gas.print_statictics(-1)
    gas.display_average_gas_prices_graph()
    gas.draw_plot()
