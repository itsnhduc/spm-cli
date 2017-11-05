import os
import json
import pickle


def main(args):
    # create pkg storing directory
    if not os.path.exists('.spm'):
        os.makedirs('.spm')
    else:
        print('.spm already exists.')

    # create pkg management file
    spmFilePath = 'spm.json'
    if spmFilePath not in os.listdir(os.getcwd()):
        spmInfo = {'dep': {}}
        with open(spmFilePath, 'w') as spmFile:
            json.dump(spmInfo, spmFile, sort_keys=True, indent=2)
    else:
        print('spm.json already exists.')

    # final output
    print('Initiation completed successfully.')
