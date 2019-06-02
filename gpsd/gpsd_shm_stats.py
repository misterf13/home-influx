#!/usr/bin/env python3
from optparse import OptionParser

import shmgpsd
import json

def get_shm():
  return shmgpsd.SHM()

def get_visible_sats(shm_gpsd):
  return shm_gpsd.satellites_visible

def get_used_sats(shm_gpsd):
  return shm_gpsd.satellites_used

def get_fix(shm_gpsd):
  return shm_gpsd.fix.mode

def get_satellites(shm_gpsd):
  sat_dict = {}
  for sat_i in range(0, shmgpsd.MAXCHANNELS):
    if shm_gpsd.skyview[sat_i].PRN != 0:
      sat_dict.update({shm_gpsd.skyview[sat_i].PRN : { 'snr':  shm_gpsd.skyview[sat_i].ss }})
  return sat_dict

def main():
  gpsd_dict = {}
  shm_gpsd  = get_shm()
  sats      = get_visible_sats(shm_gpsd)
  sats_used = get_used_sats(shm_gpsd)
  fix       = get_fix(shm_gpsd)
  gpsd_dict['fix']          = fix
  gpsd_dict['sats_visible'] = sats
  gpsd_dict['sats_used']    = sats_used
  gpsd_dict['satellite']   = get_satellites(shm_gpsd)

  print(json.dumps(gpsd_dict, indent=2))

if __name__ == '__main__':
  main()
