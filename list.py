import json


def main(args):
    with open('spm.json', 'r+') as spmFile:
        spmInfo = json.load(spmFile)
        for pkgName, pkgVersion in spmInfo['dep'].items():
            print('| * {}@{}'.format(pkgName, pkgVersion))
