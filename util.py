import requests
import subprocess
import json

def searchPkg(query):
  path = 'http://localhost:3000/api/spmpackages?filter[where][name][regexp]=' + query
  res = requests.get(path)
  return res.json()

def installPkg(pkgName):
  # find package
  searchRes = searchPkg(pkgName)
  if len(searchRes) == 0:
    print('No such package.')
    quit()
  pkgInfo = searchRes[0]

  # q: handle duplicate/upgrade/damaged
  # clone pkg
  print('Installing {}...'.format(pkgName))
  cloneUrl = pkgInfo['clone_url']
  clonePath = './.spm/' + pkgInfo['name']
  subprocess.call(
    'git clone {} {}'.format(cloneUrl, clonePath),
    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

  # write to spm.json
  with open('spm.json', 'r+') as spmFile:
    spmInfo = json.load(spmFile)
    spmInfo['dep'][pkgInfo['name']] = pkgInfo['version']
    spmFile.seek(0)
    spmFile.truncate()
    json.dump(spmInfo, spmFile, sort_keys=True, indent=2)

  # output
  print('|  + ' + pkgInfo['name'] + '@' + pkgInfo['version'])

def installFromInfo():
  with open('spm.json', 'r+') as spmFile:
    spmInfo = json.load(spmFile)
    for pkgName in spmInfo['dep']:
      installPkg(pkgName)
    print('{} package(s) installed'.format(len(spmInfo['dep'])))