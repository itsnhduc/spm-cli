import sys
import json

import requests

if len(sys.argv) == 1:
  print('Filter missing.')
  quit()
query = sys.argv[1]
if len(query) == 0:
  print('Filter missing.')
  quit()

path = 'http://localhost:3000/api/spmpackages?filter[where][name][regexp]=' + query
res = requests.get(path)
listing = res.json()

print(str(len(listing)) + ' package(s) found.')
for pkgInfo in listing:
  pkgShortInfo = '|  ' + pkgInfo['name'] + '@' + pkgInfo['version']
  print(pkgShortInfo)

# q: find with author