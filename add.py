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
    pkgInfo = util.getPkg(pkgName)
    if pkgInfo is None:
        print('No such package.')
        quit()

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
    path = util.apiUrl(pkgInfo['id'])
    requests.put(path, data=newPkgInfo)


def installFromInfo():
    with open('spm.json', 'r+') as spmFile:
        spmInfo = json.load(spmFile)
        for pkgName in spmInfo['dep']:
            installPkg(pkgName)
        print('{} package(s) installed'.format(len(spmInfo['dep'])))
