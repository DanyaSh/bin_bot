from urllib.request import urlopen
import json
import time
import datetime

base_pair = 'BTCUSDT'
depend_pair = 'ETHUSDT'
t_end = time.time_ns()//1000000
t_start = t_end-3600000
kl_interval = '1m' #1m • 3m • 5m • 15m • 30m • 1h • 2h • 4h • 6h • 8h • 12h • 1d • 3d • 1w • 1M

def create_dict(list):
    list_answer = []
    for x in list:
        dict_answer = {}
        dict_answer['type']='up' if float(x[1])<float(x[4]) else 'down'
        dict_answer['amplitude'] = abs(float(x[2])-float(x[3])) / (float(x[1])/100) 
        list_answer.append(dict_answer)
    return list_answer

while base_pair:
        #get klines last hour
        get_klines_base = f"https://api.binance.com/api/v3/klines?symbol={base_pair}&interval={kl_interval}&startTime={t_start}&endTime={t_end}"
        data = urlopen(get_klines_base).read()
        d_base = json.loads(data)
        get_klines_depend = f"https://api.binance.com/api/v3/klines?symbol={depend_pair}&interval={kl_interval}&startTime={t_start}&endTime={t_end}"
        data = urlopen(get_klines_base).read()
        d_depend = json.loads(data)

        #create list_dict from list_list
        stack_base = create_dict(d_base)
        stack_depend = create_dict(d_depend)

        #compare lists base(n) with depend(n+1)
        list_result = []
        for x in range(len(stack_base)-1):
            if stack_base[x]['type'] == stack_depend[x+1]['type']:
                if stack_base[x]['amplitude']*0.5 <= stack_depend[x+1]['amplitude'] <= stack_base[x]['amplitude']*1.5:
                    continue
            list_result.append(float(d_depend[x][1]))

        #if change more than 1 %
        change = max(list_result)-min(list_result)
        most_change = change/(min(list_result)/100)
        print(datetime.datetime.now(), most_change) if most_change>= 1 else print(datetime.datetime.now(), ' program is running', end = '\r')
        time.sleep(15)