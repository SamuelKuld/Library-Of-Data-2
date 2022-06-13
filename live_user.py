from platform import java_ver
import time
import datetime as dt
import os
import pylab as plt
import gas
gas = gas.gas_money()
plt.ion()


def clear():
    os.system("cls")


states = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska',
          'nevada', 'new-hampshire', 'new-jersey', 'new-mexico', 'new-york', 'north-carolina', 'north-dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode-island', 'south-carolina', 'south-dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'washington-dc', 'west-virginia', 'wisconsin', 'wyoming']
#states = ["\n".join(wrap(state, 5)) for state in states]


def main():
    gas.read_gas_prices()
    print("Welcome to the Gas Price Tester")
    print("Current Time : " + time.strftime("%H:%M:%S"))
    print("Plots : ")
    records = len(gas.prices) * 51
    print(f"  {records} records total")
    print(f"  {len(gas.prices)} timeframes total")

    print("General information:")
    print(f"  {len(gas.prices[0])} states total")
    total_prices = []
    for i in gas.prices:
        for j in i:
            total_prices.append(float(j.price.replace('$', '')))
    print(
        f"  {sum(total_prices) / records} All Time Gas price average")
    print(
        f"  {sum([float(i.price.replace('$', '')) for i in gas.prices[-1]]) / 51} Last Time Frame Average")
    print(
        "  " + str(dt.datetime.fromtimestamp(round(float(gas.prices[-1][-1].time_)))) + " Last Time Frame")
    print(
        f"Expect roughly {(float(gas.prices[-1][-1].time_) - float(gas.prices[-1][0].time_)) / 60} minutes between each update")
    print("Time from last Time Frame:" + str(dt.datetime.now() - dt.datetime.fromtimestamp(
        round(float(gas.prices[-1][-1].time_)))))

    old = 0
    avg_prices = []
    times = []
    for record in gas.prices:
        for i in record:
            old += float(i.price.replace('$', ''))
        record_time = dt.datetime.fromtimestamp(round(float(record[0].time_)))
        times.append(record_time)
        avg_prices.append(old / 51)
        old = 0
    plt.plot(times[::-1][:5], avg_prices[::-1][:5])
    plt.draw()
    plt.pause(1)


while True:
    clear()
    main()
