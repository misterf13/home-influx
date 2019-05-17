from datetime import datetime
from influxdb import InfluxDBClient

import subprocess

def get_time():
  current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

  return current_time

def add_tag(list_to_tag, tag):
  for item in list_to_tag:
    item['measurement'] = tag

def str_to_num(num_string):
  match = num_re.match(num_string)
  if match:
    num = float(match.group())
  else:
    # Return fake value so nothing breaks
    printf('No match found! Bad data going to influx.')
    num = 0.0

  return num

client = InfluxDBClient(host='capsule2', port=32774)
client.create_database('nut')
client.switch_database('nut')

nut_output  = subprocess.check_output(['upsc', 'cyberpower1'])
# This removes the last newline
nut_decoded = nut_output.decode('utf-8').rstrip('\n')
# Use newline to split into values
nut_list = nut_decoded.split('\n')

data_dict = {'fields':{}}
for info in nut_list:
  key, _val = info.split(':')
  try:
    val = float(_val)
  except:
    val = _val
  data_dict['fields'].update({key:val})

data_dict['measurement'] = 'CyberPower'
data_dict['time'] = get_time()

client.write_points([data_dict])
