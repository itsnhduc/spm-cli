import pickle

def setState(key, value):
  with open('.spm/states.spm', 'rb+') as sttFile:
    states = pickle.load(sttFile)
    states[key] = value
    sttFile.seek(0)
    sttFile.truncate()
    pickle.dump(states, sttFile)
    
def getState(key):
  with open('.spm/states.spm', 'rb') as sttFile:
    states = pickle.load(sttFile)
    return states[key]