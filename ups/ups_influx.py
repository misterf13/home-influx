from datetime import datetime
from influxdb import InfluxDBClient

import subprocess

def setup_influx(influx_host, influx_port):
  client = InfluxDBClient(host=influx_host, port=influx_port)
  client.create_database('nut')
  client.switch_database('nut')

  return client

def send_to_influx(influx_client, nuts):
  data_dict = {'fields':{}}
  for info in nuts:
    print(info)
    key, _val = info.split(':')[0:2]
    try:
      val = float(_val)
    except:
      val = _val
    data_dict['fields'].update({key:val})

  data_dict['measurement'] = 'CyberPower'
  data_dict['time'] = get_time()

  print("Writing: {}".format(data_dict))
  influx_client.write_points([data_dict])

def get_nut():
  nut_output  = subprocess.check_output(['upsc', 'cyberpower1'])
  # This removes the last newline
  nut_decoded = nut_output.decode('utf-8').rstrip('\n')
  # Use newline to split into values
  nut_list = nut_decoded.split('\n')

  return nut_list

def get_time():
  current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

  return current_time

def main():
  influx_client = setup_influx('capsule2', 32774)
  nut_list = get_nut()
  send_to_influx(influx_client, nut_list)

if __name__ == '__main__':
  main()
