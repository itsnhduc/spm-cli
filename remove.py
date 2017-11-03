import requests
import json
import shutil
import util
import os
import stat


def main(args):
    # check empty pkg name
    if len(args) == 0:
        print('Package name missing.')
        quit()

    # get pkg info
    pkgInfo = util.getPkg(args[0])
    if pkgInfo is None:
        print('No such package.')
        quit()
    curName = pkgInfo['name']

    # check if in spm.json
    with open('spm.json', 'r+') as spmFile:
        spmInfo = json.load(spmFile)
        if curName not in spmInfo['dep']:
            print('Package not installed yet.')
            quit()
        curVer = spmInfo['dep'][curName]
        spmInfo['dep'].pop(pkgInfo['name'], None)
        spmFile.seek(0)
        spmFile.truncate()
        json.dump(spmInfo, spmFile, sort_keys=True, indent=2)

    # remove
    print('Removing {}...'.format(pkgInfo['name']))
    shutil.rmtree('./.spm/{}'.format(pkgInfo['name']), onerror=onerror)

    # output
    pkgInfoStr = '{}@{}'.format(curName, curVer)
    print('|  - {}'.format(pkgInfoStr))

    # decrease install count
    modifyInfo = {'install_count': pkgInfo['install_count'] - 1}
    path = util.apiUrl(pkgInfo['_id'])
    requests.put(path, data=modifyInfo)


def onerror(fn, path, excInfo):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        fn(path)
    else:
        print(excInfo)
