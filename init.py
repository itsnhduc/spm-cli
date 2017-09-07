import os
import json

# create pkg storing directory
if not os.path.exists('.spm'):
  os.makedirs('.spm')
  print('.spm created.')
else:
  print('.spm already exists.')

# create pkg management file
spmFilePath = 'spm.json'
if spmFilePath not in os.listdir():
  spmInfo = { 'dep': {} }
  with open(spmFilePath, 'w') as spmFile:
    json.dump(spmInfo, spmFile, sort_keys=True, indent=2)
  print('spm.json created.')
else:
  print('spm.json already exists.')