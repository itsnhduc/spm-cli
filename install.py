import sys
import json
import os

import requests

import util

# get pkg name
if len(sys.argv) == 1:
  util.installFromInfo()
else:
  pkgName = 'spm-pkg-' + sys.argv[1]
  if len(pkgName) == 0:
    print('Package name missing.')
    quit()
  else:
    util.installPkg(pkgName)