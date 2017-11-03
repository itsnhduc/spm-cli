import subprocess
import json
import util
import requests
import os

def main(args):
    if len(args) == 0:
        installFromInfo()
    else:
        pkgInfo = args[0].split('@')
        pkgName = 'spm-pkg-' + pkgInfo[0]
        pkgVersion = pkgInfo[1] if len(pkgInfo) > 1 else None
        if len(pkgName) == 0:
            print('Package name missing.')
            quit()
        else:
            installPkg(pkgName, pkgVersion)


def installPkg(pkgName, version = None):
    # find package
    pkgInfo = util.getPkg(pkgName)
    if pkgInfo is None:
        print('No such package.')
        quit()
    allVer = [c['version'] for c in pkgInfo['commits']]
    curVer = version if (version is not None) and (version in allVer) else allVer[0]
    curSha = [c for c in pkgInfo['commits'] if c['version'] == curVer][0]['sha']
    curName = pkgInfo['name']
    incCountFlag = False

    # check & write spm.json
    with open('spm.json', 'r+') as spmFile:
        spmInfo = json.load(spmFile)
        if curName in spmInfo['dep']:
            if spmInfo['dep'][curName] == curVer:
                print('Package up-to-date')
                quit()
            print('Updating package version from {} to {}'.format(spmInfo['dep'][curName], curVer))
        spmInfo['dep'][curName] = curVer
        spmFile.seek(0)
        spmFile.truncate()
        json.dump(spmInfo, spmFile, sort_keys=True, indent=2)
    
    # remove current version & clone updated version
    cloneUrl = pkgInfo['clone_url']
    clonePath = '.\\.spm\\' + curName
    if os.path.isdir(clonePath):
        # already cloned
        print('Pull updates from remote of {}...'.format(curName))
        subprocess.call('git pull origin master',
            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    else:
        # fresh clone
        print('Cloning {}...'.format(curName))
        incCountFlag = True
        subprocess.call('git clone {} {}'.format(cloneUrl, clonePath),
            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


    # checkout to version
    print('Checking out v{}...'.format(curVer))
    os.chdir(os.getcwd() + clonePath[1:])
    subprocess.call('git checkout {}'.format(curSha),
        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # output
    pkgInfoStr = '{}@{}'.format(curName, curVer)
    print('|  + {}'.format(pkgInfoStr))

    # increase install count
    if incCountFlag:
        modifyInfo = {'install_count': pkgInfo['install_count'] + 1}
        path = util.apiUrl(pkgInfo['_id'])
        requests.put(path, data=modifyInfo)


def installFromInfo():
    with open('spm.json', 'r+') as spmFile:
        spmInfo = json.load(spmFile)
        for pkgName in spmInfo['dep']:
            installPkg(pkgName, spmInfo['dep'][pkgName])
        print('{} package(s) installed'.format(len(spmInfo['dep'])))
