import sys
import json
import os
import re

import requests

# verify pkg
hasDocs = 'docs' in os.listdir()
if not hasDocs:
  print('Package Rejected: No documentation found.')
  quit()
# q: what if publishing package.json to server?
# q: more verification needed
# q: handle dublicate

# read repo info
path = os.getcwd() + '\\package.json'
with open(path) as f:
  pkgJson = json.load(f)
  info = {
    'name': pkgJson['name'],
    'version': pkgJson['version'],
    'author': pkgJson['author'],
    'description': pkgJson['description'],
    'docs_url': 'https://{}.github.io/{}/'.format(pkgJson['author'], pkgJson['name']),
    'clone_url': 'https://github.com/{}/{}.git'.format(pkgJson['author'], pkgJson['name']),
    'tarball_url': 'https://github.com/{}/{}/tar/master'.format(pkgJson['author'], pkgJson['name'])
  }

# save reference
res = requests.post('http://localhost:3000/api/spmpackages', data = info)
if res.status_code == 200:
  print("Package published successfully.")