from bs4 import BeautifulSoup as bs
from datetime import datetime
from influxdb import InfluxDBClient

import re
import urllib3
import sys

num_re = re.compile(r'[-+]?[0-9]+(\.[0-9]*)?')

def get_arris_status(page):
  http = urllib3.PoolManager()
  r    = http.request('GET', 'http://192.168.100.1/' + page)
  if r.status == 200:
    return r
  else:
    print('Error in request: {0}'.format(r.status))
    sys.exit(1)

def setup_influx(influx_host, influx_port):
  client = InfluxDBClient(host=influx_host, port=influx_port)
  client.create_database('arris')
  client.switch_database('arris')

  return client

def get_time():
  current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

  return current_time

def str_to_num(num_string):
  match = num_re.match(num_string)
  if match:
    num = float(match.group())
  else:
    # Just return the string
    num = num_string

  return num

def process_html_table(html_table_data):
  header      = html_table_data.find('th')
  header_text = header.get_text()
  # Here we skip the first <tr> which have the table headers
  rows        = html_table_data.find_all('tr')[1:]
  tabled_data = []
  for row in rows:
    cols = row.find_all('td')
    cols = [item.text.strip() for item in cols]
    tabled_data.append([item for item in cols if item])

  return tabled_data

def process_table(client, data, tag, float_it_up=True):
  headers   = data.pop(0)
  list_dict = []
  data_time = get_time()
  for stat in data:
    data_dict = {'fields':{},
                 'tags'  :{}}
    for index, header in enumerate(headers):
      try:
        stat[index]
      except:
        print('No value for index: {0}'.format(index))
        continue
      # Turn fields to floats if set
      if float_it_up:
        val = str_to_num(stat[index])
      else:
        val = stat[index]
      # We want Procedure, Channel, and Channel ID as tags instead of fields
      if header in ['Procedure', 'Channel', 'Channel ID']:
        data_dict['tags'].update({header:val})
      else:
        data_dict['fields'].update({header:val})
      data_dict['measurement'] = tag
      data_dict['time']        = data_time
    print('Writing: {}'.format(data_dict))
    client.write_points([data_dict])

def main():
  status_uri = 'cmconnectionstatus.html'
  # We can get uptime from cmswinfo.html
  info_uri   = 'cmswinfo.html'
  url_ret    = get_arris_status(status_uri)
  soup       = bs(url_ret.data, 'lxml')
  tables     = soup.findAll('table', attrs={'class':'simpleTable'})

  # Setup influx client
  influx_client = setup_influx('capsule2', 32774)

  soup_dict = {}
  for table_index, info in enumerate(['startup', 'downstream', 'upstream']):
    soup_dict[info] = soup.select('table')[table_index]

  for header in soup_dict:
    table_info = process_html_table(soup_dict[header])
    if header == 'startup':
      process_table(influx_client, table_info, header, float_it_up=False)
    else:
      process_table(influx_client, table_info, header)

if __name__ == '__main__':
  main()
