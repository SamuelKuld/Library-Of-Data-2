import time
import gas
import CA_gas
import utils.multi_threader as multi_threader


def load():
    pass


def gas_thread(test=False):
    gas_data = gas.gas_money()
    while True:
        gas_data.get_gas_prices()
        gas_data.save_gas_prices()
        if test:
            break


def CA_gas_thread(test=False):
    CA_gas_data = CA_gas.gas_money()

    while True:
        CA_gas_data.get_gas_prices()
        CA_gas_data.save_gas_prices()
        if test:
            break


# def gpu_thread():
    # gpu_data = gpu.gpu_analyzer()
    # gpu_thread = multi_threader.Thread(gpu_data.get_gpu_prices)
    # while True:
        # gpu_thread.start()


def main():
   # thread3 = multi_threader.Thread(gpu_thread)
    thread1 = multi_threader.Thread(gas_thread)
    thread2 = multi_threader.Thread(CA_gas_thread)
    while True:
        thread1.start()
        thread2.start()
        # thread3.start()


if __name__ == '__main__':
    load()
    main()
