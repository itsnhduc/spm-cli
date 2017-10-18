import sys
import json

import util

def main(args):
  if len(args) == 0:
    print('Filter missing.')
    quit()
  query = args[0]

  listing = util.searchPkg(query)

  print(str(len(listing)) + ' package(s) found.')
  for pkgInfo in listing:
    pkgShortInfo = '|  ' + pkgInfo['name'] + '@' + pkgInfo['version']
    print(pkgShortInfo)

  # q: find with author