'''
@file 
Parses a config file

Checks if a config file exists.  If it does, it loads the contents into
a dictionary accesible by the simulator.  If it doesn't, the dictionary
is populated by default values, which are written to a new config file.

@TODO
Set actual default settings
'''

import json

def write(dictionary, filename='config.json'):
  fp = open(filename,'w')
  json.dump(dictionary, fp, sort_keys=True, indent=2)
  fp.close()

def read(filename='config.json'):
  # Declare default settings
  settings = {
    "key" : "value",
  }

  # Try to load the config file and merge into settings
  try:
    fp = open(filename,'r')
    customSettings = json.load(fp)
    settings.update(customSettings)
    fp.close()
  except IOError:
    print "No config file, using defaults"

  return settings

