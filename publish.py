import json
import os
import re
import datetime
import requests

import util


def main(args):
    # verify pkg
    hasDocs = 'docs' in os.listdir(os.getcwd())
    if not hasDocs:
        print('Package Rejected: No documentation found.')
        quit()

    # read repo info
    path = os.getcwd() + '/package.json'
    with open(path) as f:
        pkgJson = json.load(f)

        curAuthor = pkgJson['author']
        curName = pkgJson['name']
        curDesc = pkgJson['description']
        curVer = pkgJson['version']

        generalInfo = requests.get('https://api.github.com/repos/{}/{}'.format(curAuthor, curName)).json()
        commits = requests.get('https://api.github.com/repos/{}/{}/commits'.format(curAuthor, curName)).json()
        curSha = commits[0]['sha']

        pkgEntry = util.getPkg(curName)

        if pkgEntry is None:
            # new package
            info = {
                'name': curName,
                'author': curAuthor,
                'description': curDesc,
                'language': generalInfo['language'],
                'clone_url': 'https://github.com/{}/{}.git'.format(curAuthor, curName),
                'docs_url': 'https://{}.github.io/{}/'.format(curAuthor, curName),
                'tarball_url': 'https://github.com/{}/{}/tarball/master'.format(curAuthor, curName)
            }
            # create new entry
            res = requests.post(util.apiUrl(), data=info)
            if res.status_code == 200:
                print('New package recorded.')
                pkgEntry = res.json()
            else:
                print('Error publishing new package')
                print(res)
        else:
            # existing package, new version
            latestVer = pkgEntry['commits'][0]['version']
            latestSha = pkgEntry['commits'][0]['sha']
            if latestVer == curVer:
                print('Duplicate version number detected. Did you forget to modify package.json?')
                return
            if latestVer > curVer:
                print('Older version detected. Is there a typo in your version number?')
                return
            if latestSha == curSha:
                print('Duplicate commit detected. Did you forget to push your code to GitHub?')
                return

        newCommit = {'version': curVer, 'sha': curSha}
        path = util.apiUrl('{}/commits'.format(pkgEntry['_id']))
        commRes = requests.post(path, data=newCommit)
        if commRes.status_code != 200:
            print('Error publishing version')
        print('Published version {}'.format(curVer))

    
