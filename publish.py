import json
import os
import re
import datetime
import requests

def main(args):
  # verify pkg
  hasDocs = 'docs' in os.listdir()
  if not hasDocs:
    print('Package Rejected: No documentation found.')
    quit()
    
  # q: handle duplicate

  # read repo info
  path = os.getcwd() + '\\package.json'
  with open(path) as f:
    pkgJson = json.load(f)
    info = {
      'name': pkgJson['name'],
      'version': pkgJson['version'],
      'author': pkgJson['author'],
      'description': pkgJson['description'],
      'clone_url': 'https://github.com/{}/{}.git'.format(pkgJson['author'], pkgJson['name']),
      'docs_url': 'https://{}.github.io/{}/'.format(pkgJson['author'], pkgJson['name']),
      'tarball_url': 'https://github.com/{}/{}/tarball/master'.format(pkgJson['author'], pkgJson['name'])
    }

  # save reference
  res = requests.post('http://localhost:3000/api/spmpackages', data = info)
  if res.status_code == 200:
    print("Package published successfully.")