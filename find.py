import sys
import json

import util


def main(args):
    if len(args) == 0:
        print('Filter missing.')
        quit()
    args = sorted(args)
    query = args[-1]

    listing = []
    if '--author' in args:
        listing = util.getPkgByAuthor(query)
    else:
        listing = util.searchPkg(query)

    print(str(len(listing)) + ' package(s) found.')
    for pkgInfo in listing:
        curName = pkgInfo['name']
        latestVer = pkgInfo['commits'][0]['version']
        pkgShortInfo = '|  {} (latest={})'.format(curName, latestVer)
        print(pkgShortInfo)
