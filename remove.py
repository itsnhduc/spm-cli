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

    # check if in spm.json
    with open('spm.json', 'r+') as spmFile:
        spmInfo = json.load(spmFile)
        spmInfo['dep'].pop(pkgInfo['name'], None)
        spmFile.seek(0)
        spmFile.truncate()
        json.dump(spmInfo, spmFile, sort_keys=True, indent=2)

    # remove
    print('Removing {}...'.format(pkgInfo['name']))
    shutil.rmtree('./.spm/{}/'.format(pkgInfo['name']), onerror=onerror)

    # output
    print('|  - ' + pkgInfo['name'] + '@' + pkgInfo['version'])

    # decrease install count
    newPkgInfo = pkgInfo.copy()
    newPkgInfo['install_count'] = pkgInfo['install_count'] - 1
    path = util.apiUrl(pkgInfo['id'])
    requests.put(path, data=newPkgInfo)


def onerror(fn, path, excInfo):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        fn(path)
    else:
        print('An unknown error has occured.')
