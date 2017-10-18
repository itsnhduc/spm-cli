import requests

def searchPkg(query, exact=False):
  exactStr = '' if exact else '[regexp]'
  queryStr = ('spm-pkg-' if 'spm-pkg-' not in query else '') + query
  path = 'http://localhost:3000/api/spmpackages?filter[where][name]' + exactStr + '=' + queryStr
  res = requests.get(path)
  return res.json()