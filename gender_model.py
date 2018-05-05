import numpy as np
from keras.preprocessing import sequence
from keras.models import load_model
model = load_model('char_rnn_model.h5')

char2idx = {'o': 0, 'b': 1, 'e': 2, 'w': 3, 'p': 4, '-': 5, 't': 6, 'k': 7, 'q': 8, 'f': 9, 'n': 10, 'z': 11, 'u': 12, ' ': 13, '.': 14, 'd': 15, 'h': 16, 'm': 17, '(': 18, 'r': 19, ')': 20, 'j': 21, 'l': 22, 'i': 23, 's': 24, 'c': 25, 'a': 26, 'g': 27, ':': 28, 'v': 29, 'y': 30, 'x': 31}
idx2char = {0: 'o', 1: 'b', 2: 'e', 3: 'w', 4: 'p', 5: '-', 6: 't', 7: 'k', 8: 'q', 9: 'f', 10: 'n', 11: 'z', 12: 'u', 13: ' ', 14: '.', 15: 'd', 16: 'h', 17: 'm', 18: '(', 19: 'r', 20: ')', 21: 'j', 22: 'l', 23: 'i', 24: 's', 25: 'c', 26: 'a', 27: 'g', 28: ':', 29: 'v', 30: 'y', 31: 'x'}

# Converts a name into vector
def name2vector(name):
    chars = list(name)
    vector = [ char2idx[c] for c in chars ]
    return np.array(vector)

# Converts names to fixed size tensor
def names2tensor(names, maxlen=25):
    namelist = [name2vector(name) for name in names]
    return sequence.pad_sequences(np.array(namelist), maxlen=maxlen)  # root of all troubles

def nameTest(name):
  result = model.predict_classes(np.array(names2tensor([name.lower()])))[0][0]
  if result:
    print("Male")
  else:
    print("Female")

def isMale(name):
  result = model.predict_classes(np.array(names2tensor([name.lower()])))[0][0]
  return result

def genderCount(fileName):
  # read file line by line
  # count each gender type
  f = open("output.txt", "w")
  with open(fileName, "r") as myFile:
    total = 0
    maleCount = 0
    femaleCount = 0
    for line in myFile:
      line = line.rstrip()
      if len(line) > 1:
        f.write(line)
        if isMale(line):
          maleCount+=1
          f.write(" - M")
        else:
          femaleCount+=1
          f.write(" - F")
        f.write("\n")
      #print(i, len(line))
      total+=1
  s = "Total: " + str(total)+"\nMale: "+str(maleCount)+"\nFemale: "+str(femaleCount)
  print(s)
  f.write("\n########\n")
  f.write(s)

# python gender_model.py
genderCount("input_names.txt")