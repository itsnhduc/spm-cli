import requests
import os


def apiUrl(tail = ''):
    apiHost = os.environ.get('API_HOST', 'localhost')
    apiPort = os.environ.get('API_PORT', '3000')
    endPoint = 'api/pkgs/'
    return 'http://{}:{}/{}{}'.format(apiHost, apiPort, endPoint, tail)


def searchPkg(query):
    queryStr = ('spm-pkg-' if 'spm-pkg-' not in query else '') + query
    path = apiUrl('?name={}'.format(queryStr)) 
    res = requests.get(path)
    return res.json()

def getPkg(name):
    searchRes = searchPkg(name)
    if len(searchRes) > 0:
        return searchRes[0]
    else:
        return None