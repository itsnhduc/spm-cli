import sys
import json

import requests

import util
import state

# parse arg
if len(sys.argv) == 1:
  print('Package name missing.')
  quit()
pkgName = sys.argv[1]

# check if already starred
starListing = state.getState('star')
if pkgName in starListing:
  print('Package {} already starred.'.format(pkgName))
  quit()

# search for pkg
searchRes = util.searchPkg(pkgName, exact=True)
if len(searchRes) == 0:
  print('No such package.')
  quit()
pkgInfo = searchRes[0]

# add star
path = 'http://localhost:3000/api/spmpackages/{}'.format(pkgInfo['id'])
newPkgInfo = pkgInfo.copy()
newPkgInfo['star_count'] = pkgInfo['star_count'] + 1
requests.put(path, data=newPkgInfo)

# update to state
starListing.append(pkgName)
state.setState('star', starListing)

# final logging
print('Package {} starred ({} currently).'.format(pkgName, pkgInfo['star_count'] + 1))