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
import math

def write(dictionary, filename='config.json'):
  fp = open(filename,'w')
  json.dump(dictionary, fp, sort_keys=True, indent=2)
  fp.close()

def read(filename='config.json'):
  # Declare default settings
  settings = {
    "BIN" : {
      "MAX_X" : 100,
      "MAX_Y" : 100,
      "MAX_Z" : 100,
    },
    "FOREST" : {
      "DIMENSIONS" : {
        "MAX_X" : 1000,
        "MAX_Y" : 1000,
        "MAX_Z" : 1000,
      },
      "SURFACE_DENSITY" : 0.02,
    },
    "NODE" : {
      "NODE_MASS" : 1.0,
      "MEAN_RADIUS" : 4.0,
      "MIN_RADIUS" : 2.0,
      "MAX_RADIUS" : 6.0,
      "SIGMA_RADIUS" : .45,
    },
    "TUBE": {
      "SEGMENT_LENGTH" : 8.0,
      "SEGMENT_NUM" : 50,
    },
    "SIMULATION" : {
      "TIME_STEP" : .01,
      "MIN_DIST" : .001,
      "ATTRACT_RADIUS" : 3,
      "GRAVITY" : .1,
      "GROWTH_SPEED" : 10.2,
    },
    "SPRINGS" : {
      "ANGLES" : {
        "MAX_THETA" : 2*math.pi,
        "MAX_PHI" : math.pi/2,
        "MEAN_PHI" : math.pi/4.0,
        "SIGMA_PHI" : 0.282387/2,
      },
      "CONSTANTS" : {
        "EDGE" : 100,
        "TORSION" : 100,
      },
      "DAMPING" : {
        "TORSION" : math.sqrt(100),
        "LINEAR" : math.sqrt(100),
      }
    }, 
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

