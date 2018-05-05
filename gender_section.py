import win_unicode_console
win_unicode_console.enable()

################################################################################
import numpy as np
from keras.preprocessing import sequence
from keras.models import load_model
model = load_model('char_rnn_model.h5')

char2idx = {'o': 0, 'b': 1, 'e': 2, 'w': 3, 'p': 4, '-': 5, 't': 6, 'k': 7, 'q': 8, 'f': 9, 'n': 10, 'z': 11, 'u': 12, ' ': 13, '.': 14, 'd': 15, 'h': 16, 'm': 17, '(': 18, 'r': 19, ')': 20, 'j': 21, 'l': 22, 'i': 23, 's': 24, 'c': 25, 'a': 26, 'g': 27, ':': 28, 'v': 29, 'y': 30, 'x': 31}
idx2char = {0: 'o', 1: 'b', 2: 'e', 3: 'w', 4: 'p', 5: '-', 6: 't', 7: 'k', 8: 'q', 9: 'f', 10: 'n', 11: 'z', 12: 'u', 13: ' ', 14: '.', 15: 'd', 16: 'h', 17: 'm', 18: '(', 19: 'r', 20: ')', 21: 'j', 22: 'l', 23: 'i', 24: 's', 25: 'c', 26: 'a', 27: 'g', 28: ':', 29: 'v', 30: 'y', 31: 'x'}


# Converts a name into vector
def name2vector(name):
	chars = list(name)
	vector = [ char2idx[c] for c in chars if c in char2idx ]
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

def genderCount(ner_person):
  # read file line by line
  # count each gender type
	#f = open("femaleNames.txt", "w")
  #with open(fileName, "r") as myFile:
	total = 0
	maleCount = 0
	femaleCount = 0
	for name in ner_person:
		name = name.rstrip()
		if len(name) > 1:
		#f.write(line)
			if isMale(name):
				maleCount+=1
				#f.write(" - M")
			else:
				femaleCount+=1
				#print(name.encode('utf-8'))
				#f.write(name)
				#f.write("\n")
	  #print(i, len(line))
		total+=1
	return femaleCount, total
  #s = "Total: " + str(total)+"\nMale: "+str(maleCount)+"\nFemale: "+str(femaleCount)
  #print(s)
  #f.write("\n########\n")
  #f.write(s)

# python gender_model.py
#genderCount("input_names.txt")



################################################################################



import sys
import json
import timeit
from datetime import datetime
from dateutil.parser import parse
#from textblob import TextBlob

start = timeit.default_timer()
start_year = 2008
end_year = 2017

def gimmeIndex(i):
	return (start_year +int(i/12))*100+int(i%12)+1

def gimmeDict():
	onedict = {}
	onedict["sum"]=0
	for i in range(0,(end_year - start_year)*12):
		index = gimmeIndex(i)
		genderDict = {}
		#genderDict["m"] = 0
		genderDict["f"] = 0
		genderDict["t"] = 0
		onedict[index] = genderDict
	return onedict



total = 0
dict={}

"""for x in range(start_year, end_year):
	for y in range(1,13):
		dict[x*100+y] = 0"""

data = "data/news_db.json"
#data = "news_db.json"
#data = "bd_news_dhaka_tribune.json"
with open(data, encoding="utf-8") as file:
	for line in file:
		parsed_json = json.loads(line)
		#content = parsed_json["content"]
		#count = content.lower().count(key)
		date = parsed_json['date_published']['$date']
		t = parse(date)
		n = t.year*100+t.month
		# MAKE A LIST OF ALL WORD IN line
		# word_list = content.lower().split()
		if n<201701:
			#word_list = TextBlob(content.lower().replace('.',' ')).words #split('#')
			# ITERATE OVER EACH WORD
			#for word in word_list:
				# IF NOT EXISTS IN dict, dict[WORD] = gimmeDict()
			section = parsed_json["section"]
			print(section)
			ner_person = parsed_json["ner_person"]
			num_person = len(ner_person)
			print(num_person)
			if section not in dict:
				dict[section] = gimmeDict()
			# INCREASE ENCOUNTER
			f, t = genderCount(ner_person)
			dict[section][n]["f"] += f
			dict[section][n]["t"] += t
			dict[section]["sum"] += t
file.close()

with open('output/gender_per_time.json', 'w') as fp:
	json.dump(dict, fp)
fp.close()

i = 1
with open("frequency.txt", "w") as freq_file:
	for x in dict:
		s = "{}:\t{}: {}\n".format(i,x,dict[x]["sum"])
		freq_file.write(s)
		i+=1
print(i-1)
freq_file.close()
# MEASURING RUNTIME
stop = timeit.default_timer()
minutes = int((stop-start)/60)
seconds = int((stop-start)%60)
print("runtime: ", minutes, "minutes", seconds, "seconds")
#print(stop-start)

##########################
#json: http://docs.python-guide.org/en/latest/scenarios/json/
#
"""with open('strings.json') as json_data:
	d = json.load(json_data)
	print(d)""" #load json directly to a dictionary

################################################################################