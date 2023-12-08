from datetime import datetime
import json

import subprocess

def json_print(nuts):
 # Split the input nuts into lines
 lines = nuts.strip().split('\n')

 # Initialize an empty dictionary
 nested_dict = {}

 # Iterate through each line and populate the nested dictionary
 for line in lines:
     try:
         keys, val_ = line.split(': ', 1)
         try:
           value = float(val_)
         except:
           value = val_
         keys = keys.split('.')

         current_dict = nested_dict
         for key in keys[:-1]:
             current_dict = current_dict.setdefault(key, {})

         current_key = keys[-1]

         if isinstance(current_dict, dict):
             current_dict[current_key] = value
     except ValueError:
         # Skip lines that don't follow the expected format
         pass

 # Print the resulting nested dictionary
 print(json.dumps(nested_dict, indent=2))

def get_nut():
  nut_output = subprocess.run(['upsc', 'cyberpower1'], capture_output=True)
  nut_text   = nut_output.stdout.decode('utf-8')
  return nut_text

def main():
  nut_text = get_nut()
  json_print(nut_text)

if __name__ == '__main__':
  main()
