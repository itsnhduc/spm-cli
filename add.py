import subprocess
import json
import util
import requests

# get pkg name
def main(args):
  if len(args) == 0:
    installFromInfo()
  else:
    pkgName = 'spm-pkg-' + args[0]
    if len(pkgName) == 0:
      print('Package name missing.')
      quit()
    else:
      installPkg(pkgName)

def installPkg(pkgName):
  # find package
  searchRes = util.searchPkg(pkgName)
  if len(searchRes) == 0:
    print('No such package.')
    quit()
  pkgInfo = searchRes[0]

  # q: handle duplicate/upgrade/damaged
  # clone pkg
  print('Adding {}...'.format(pkgName))
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

  # increase install count
  newPkgInfo = pkgInfo.copy()
  newPkgInfo['install_count'] = pkgInfo['install_count'] + 1
  path = 'http://localhost:3000/api/spmpackages/{}'.format(pkgInfo['id'])
  requests.put(path, data=newPkgInfo)

def installFromInfo():
  with open('spm.json', 'r+') as spmFile:
    spmInfo = json.load(spmFile)
    for pkgName in spmInfo['dep']:
      installPkg(pkgName)
    print('{} package(s) installed'.format(len(spmInfo['dep'])))