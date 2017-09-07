import sys
import json

import util

if len(sys.argv) == 1:
  print('Filter missing.')
  quit()
query = sys.argv[1]
if len(query) == 0:
  print('Filter missing.')
  quit()

listing = util.searchPkg(query)

print(str(len(listing)) + ' package(s) found.')
for pkgInfo in listing:
  pkgShortInfo = '|  ' + pkgInfo['name'] + '@' + pkgInfo['version']
  print(pkgShortInfo)

# q: find with author