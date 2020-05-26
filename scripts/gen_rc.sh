#! /bin/bash

# Script for generating default runtime configuration
# if it does not already exist

rc=$HOME/.vmdvizrc.json

if [ ! -f "$rc" ]; then
   cat <<EOF >$rc
{
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
  "rendering" : 
    {
      "renderer" : "Tachyon",
	  "render_extension" : "dat",
    }
}
EOF
fi
