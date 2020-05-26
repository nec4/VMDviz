#! /usr/bin/env python 

import json
import os

# Script for generating default runtime configuration
# if it does not already exist

HOME = os.path.expanduser("~")

rc = HOME + "/.vmdvizrc.json"

default_rc = {
  "styles" :
    [
      {
        "style" : "VDW 4.0 24",
        "color" : "index",
        "selection" : "all",
        "material" : "Diffuse"
      },
      {
        "style" : "Bonds 2.5 24",
        "color" : "index",
        "selection" : "all",
        "material" : "Diffuse"
      }
    ],
  "display" :
    {
    },
  "axes" :
    {
      "set_location" : 'OFF'
    },
  "colors" :
    {
    },
  "rendering" :
    {
      "renderer" : "Tachyon",
      "render_extension" : "dat"
    }
}
print(default_rc)
if not os.path.exists(rc):
    with open(rc, 'w') as jfile:
        json.dump(default_rc, jfile, indent=4)




