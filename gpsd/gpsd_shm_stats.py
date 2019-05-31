#!/usr/bin/env python3
from optparse import OptionParser

import gpsdshm

def get_shm():
  return gpsdshm.Shm()

def get_visible_sats(gpsd_shm):
  return gpsd_shm.satellites_visible

def get_used_sats(gpsd_shm):
  return gpsd_shm.satellites_used

def get_fix(gpsd_shm):
  return gpsd_shm.fix.mode

def main(sats, sats_used, gps_fix):
  gpsd_shm = get_shm()
  # GPSD has to be up
  if gpsd_shm.status and sats:
    sats = get_visible_sats(gpsd_shm)
    print('sats_vis={0}'.format(sats))
  elif gpsd_shm.status and sats_used:
    sats_used = get_used_sats(gpsd_shm)
    print('sats_used={0}'.format(sats_used))
  elif gpsd_shm.status and gps_fix:
    fix = get_fix(gpsd_shm)
    print('fix={0}'.format(fix))

if __name__ == '__main__':
  parser = OptionParser(usage='%prog [-s] [-f]', version='%prog 0.1')
  parser.add_option('-s', '--satellites', action='store_true')
  parser.add_option('-u', '--used', action='store_true')
  parser.add_option('-f', '--fix', action='store_true')
  (options, args) = parser.parse_args()
  main(options.satellites, options.used, options.fix)
