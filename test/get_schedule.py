#!/usr/bin/env python3

"""API test for schedule ranges"""

import sys, requests, json

# For testing, I created a scheduled playlist that runs from 10:00 to 20:00 every day
# on the demo instance.

# problematic:

# - same start & end date: returns many days in the past
#start = "2023-10-22"
#end = "2023-10-22"

# - end = start + 1 day: also returns the day before start even if start > 00:00 hours
#start = "2023-10-22"
#end = "2023-10-23"

# - time ranges non-functional: (need results for MY timezone)
#
# for some reason, 'T00:00:00' and 'T00:00:00+00:00' work,
# 'T00:00:00+02:00' also gives a result
# this here gives results for the 20th, 21st, and 22nd Oct
start = "2023-10-22T00:00:00+02:00"
end = "2023-10-23T00:00:00+02:00"


url = 'https://demo.azuracast.com'

result = requests.get(url + '/api/station/1/schedule',
    headers={"accept": "application/json"},
    params={"start": start, "end": end})

if result.status_code != 200:
    print("HTTP Error", result.status_code)
    sys.exit(1)

result = sorted(result.json(), key=lambda k:k["start"])

print(json.dumps(result, indent=2) + '\n')

for r in result:
    #fmt = f"{r['start'][0:10]} {r['start'][11:16]} - {r['end'][11:16]} {r['name']}"
    fmt = f"{r['start']} - {r['end']} {r['name']}"
    print(fmt)
