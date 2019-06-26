#%%
# Just for Jupyter notebook functionality
%load_ext autoreload
%autoreload 2

#%%
# Eveything we need to make a request to a lambda function
import json
import boto3
import pprint
import os
import time
from botocore.exceptions import ClientError
# This automatically loads the logged in aws session info in ~/.aws
client = boto3.client('lambda', region_name='us-east-1')
role = os.environ['ROLE']
func_name = 'fkaw'

# the worker function should return a dict with each item having a single value
def worker_func():
    cmds = {}
    # import time
    # cmds['sleep'] = (time.time() + 30) * 1000
    cmds['sleep'] = 0
    cmds['stat'] = {"argv": 1}
    cmds['io'] = {"rd": 3, "size": "1M", "cnt": 5}
    # cmds['net'] = {"server_ip": "34.227.105.44", "port": 5201}
    cmds['cpu'] = {"n": 10000}
    # cmds['cpuu'] = {"n": 3}

    payload = {}
    payload['cmds'] = cmds

    b_payload = json.dumps(payload).encode()

    client_start_time = time.time()
    response = client.invoke(
        FunctionName=func_name,
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=b_payload,
    )
    client_end_time = time.time()

    # This is how we get the payload
    r = response['Payload'].read().decode('unicode_escape')
    if r[0] == '"' and r[-1] == '"':
        r = r[1:-1]

    r_parsed = json.loads(r)

    # Get the logs of this request
    import base64

    log_result = base64.b64decode(response['LogResult']).decode()

    # print(log_result)

    for line in log_result.strip().split('\n'):
        if line.startswith('REPORT'):
            for tab in line.strip().split('\t'):
                if tab.startswith('Duration'):
                    aws_duration = float(tab.strip().split(' ')[1])
                    # print('Duration: %.2f ms'% aws_duration)
                elif tab.startswith('Billed Duration'):
                    aws_billed_duration = float(tab.strip().split(' ')[2])
                    # print('Billed Duration: %.2f ms' % aws_billed_duration)
                elif tab.startswith('Max Memory Used'):
                    aws_max_mem = float(tab.strip().split(' ')[3])
                    # print('Max Memory Used: %.2f MB' % aws_max_mem)

    ret_val = {
        'is_cold': r_parsed['stat']['exist_id'] == r_parsed['stat']['new_id'],
        'cpu_info': r_parsed['stat']['cpu_info'],
        'inst_id': r_parsed['stat']['inst_id'],
        'inst_priv_ip': r_parsed['stat']['inst_priv_ip'],
        'new_id': r_parsed['stat']['new_id'],
        'exist_id': r_parsed['stat']['exist_id'],
        'uptime': r_parsed['stat']['uptime'],
        'vm_id': r_parsed['stat']['vm_id'],
        'vm_priv_ip': r_parsed['stat']['vm_priv_ip'],
        'vm_pub_ip': r_parsed['stat']['vm_pub_ip'],
        'start_time': r_parsed['start_time'],
        'end_time': r_parsed['end_time'],
        'elapsed_time': r_parsed['elapsed_time'],
        'aws_duration': aws_duration,
        'aws_billed_duration': aws_billed_duration,
        'aws_max_mem': aws_max_mem,
        'io_speed': r_parsed['io'][0]['speed'],
        'client_start_time': client_start_time,
        'client_end_time': client_end_time,
        'client_elapsed_time': client_end_time - client_start_time,
    }
    return ret_val


all_res = []
all_res.append(worker_func())
all_res.append(worker_func())
all_res.append(worker_func())
all_res.append(worker_func())

import pandas as pd
pd.DataFrame(data=all_res)

# pprint.pprint(worker_func())

#%% 
# Testing simple functionality
from ddsl_lambda_wg.timer import *
import ddsl_lambda_wg as dwg

def worker_func2():
    return {
        'time': time.time()
    }

wg = dwg.DdslLambdaWG(worker_func=worker_func, rps=10/60, worker_thread_count=100)
wg.start_workers()


timer = TimerClass()


# for one minute, test it out
timer.tic()

wg.prepare_test()
while timer.toc() < 5*60:
    wg.fire_wait()

wg.stop_workers()

all_res = wg.get_stats()

print(len(all_res))
# pd.DataFrame(data=all_res)