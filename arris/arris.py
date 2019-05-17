from bs4 import BeautifulSoup as bs
from datetime import datetime
from influxdb import InfluxDBClient

import re
import urllib3

#num_re = re.compile('\d+(?:\.\d+)?')
num_re = re.compile(r'[-+]?[0-9]+(\.[0-9]*)?')

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
    print('No match found! Bad data going to influx.')
    num = num_string

  return num

def process_html_table(html_table_data):
  header      = html_table_data.find('th')
  header_text = header.get_text()
  rows        = html_table_data.find_all('tr')
  tabled_data = []
  for row in rows:
    cols = row.find_all('td')
    cols = [item.text.strip() for item in cols]
    tabled_data.append([item for item in cols if item])

  #FIXME Popping index 0, it is empty.
  tabled_data.pop(0)

  return tabled_data

def process_table(client, data, tag, convert_int):
  headers   = data.pop(0)
  list_dict = []
  data_time = get_time()
  for stat in data:
    data_dict = {'fields':{}}
    for index, header in enumerate(headers):
      try:
        stat[index]
      except:
        print('No value for index: {0}'.format(index))
        continue
      #if stat[index][0].isdigit() and convert_int:
      #  val = str_to_num(stat[index])
      #else:
      #  val = stat[index]
      if tag == 'startup':
        val = stat[index]
      else:
        val = str_to_num(stat[index])
      if index == 0:
        data_dict['tags'] = {header:val}
      else:
        data_dict['fields'].update({header:val})
      data_dict['measurement'] = tag
      data_dict['time']        = data_time
    print("Writing: {}".format(data_dict))
    client.write_points([data_dict])

http = urllib3.PoolManager()
r = http.request('GET', 'http://192.168.100.1/cmconnectionstatus.html')
if r.status == 200:
  soup = bs(r.data, 'lxml')

tables = soup.findAll('table', attrs={'class':'simpleTable'})

client = InfluxDBClient(host='capsule2', port=32774)
client.create_database('arris')
client.switch_database('arris')

#Startup Procedure
startup_table = soup.select('table')[0]
#Downstream Bonded Channels
downstream_table = soup.select('table')[1]
#Upstream Bonded Channels
upstream_table = soup.select('table')[2]

startup_out = process_html_table(startup_table)
process_table(client, startup_out, 'startup', False)

downstream_out = process_html_table(downstream_table)
process_table(client, downstream_out, 'downstream', True)

upstream_out = process_html_table(upstream_table)
process_table(client, upstream_out, 'upstream', True)

