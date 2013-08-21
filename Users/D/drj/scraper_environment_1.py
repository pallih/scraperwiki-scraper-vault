# Displays the launch.json file that is used to communicate variables to the process.

import os

print os.system("cat launch.json")

import json
print json.load(open("launch.json"))['scrapername']
