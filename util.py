import requests
import os


def apiUrl(tail = ''):
    apiHost = os.environ.get('API_HOST', 'localhost')
    apiPort = os.environ.get('API_PORT', '3000')
    endPoint = 'api/pkgs/'
    return 'http://{}:{}/{}{}'.format(apiHost, apiPort, endPoint, tail)


def searchPkg(query):
    path = apiUrl('?name_regex={}'.format(query))
    res = requests.get(path)
    return res.json()

def getPkgByAuthor(author):
    path = apiUrl('?author={}'.format(author))
    res = requests.get(path)
    return res.json()

def getPkg(name):
    path = apiUrl('?name={}'.format(name))
    resJson = requests.get(path).json()
    return resJson[0] if len(resJson) > 0 else None