#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv

check_list = ["URN", "SCHNAME", "POSTCODE", "RATPUPTEA", "PSENSAP", "PNUMFSMEVER"]
keep_list = ["", "", "", "", "", ""]

check = int(sys.argv[1])
keep = int(sys.argv[2])

out = csv.writer(sys.stdout)

for root, _, files in os.walk("data/free-schools"):
    for f in files:
        if not f.endswith(".csv"):
            continue

        data = os.path.join(root, f)

        with open(data, 'r')  as input:
            table = csv.reader(input)

            keep_list = []
            for row in table:
                print row
                check_field = row[check]
                if check_field in check_list:
                    keep_list[check_list.index(check_field)] = row[keep].replace("%", "")
            out.writerow(keep_list)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv

check_list = ["URN", "SCHNAME", "POSTCODE", "RATPUPTEA", "PSENSAP", "PNUMFSMEVER"]
keep_list = ["", "", "", "", "", ""]

check = int(sys.argv[1])
keep = int(sys.argv[2])

out = csv.writer(sys.stdout)

for root, _, files in os.walk("data/free-schools"):
    for f in files:
        if not f.endswith(".csv"):
            continue

        data = os.path.join(root, f)

        with open(data, 'r')  as input:
            table = csv.reader(input)

            keep_list = []
            for row in table:
                print row
                check_field = row[check]
                if check_field in check_list:
                    keep_list[check_list.index(check_field)] = row[keep].replace("%", "")
            out.writerow(keep_list)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv

check_list = ["URN", "SCHNAME", "POSTCODE", "RATPUPTEA", "PSENSAP", "PNUMFSMEVER"]
keep_list = ["", "", "", "", "", ""]

check = int(sys.argv[1])
keep = int(sys.argv[2])

out = csv.writer(sys.stdout)

for root, _, files in os.walk("data/free-schools"):
    for f in files:
        if not f.endswith(".csv"):
            continue

        data = os.path.join(root, f)

        with open(data, 'r')  as input:
            table = csv.reader(input)

            keep_list = []
            for row in table:
                print row
                check_field = row[check]
                if check_field in check_list:
                    keep_list[check_list.index(check_field)] = row[keep].replace("%", "")
            out.writerow(keep_list)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv

check_list = ["URN", "SCHNAME", "POSTCODE", "RATPUPTEA", "PSENSAP", "PNUMFSMEVER"]
keep_list = ["", "", "", "", "", ""]

check = int(sys.argv[1])
keep = int(sys.argv[2])

out = csv.writer(sys.stdout)

for root, _, files in os.walk("data/free-schools"):
    for f in files:
        if not f.endswith(".csv"):
            continue

        data = os.path.join(root, f)

        with open(data, 'r')  as input:
            table = csv.reader(input)

            keep_list = []
            for row in table:
                print row
                check_field = row[check]
                if check_field in check_list:
                    keep_list[check_list.index(check_field)] = row[keep].replace("%", "")
            out.writerow(keep_list)
