import sys
import json
import timeit
from datetime import datetime
from dateutil.parser import parse
from textblob import TextBlob

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
		onedict[index] = 0
	return onedict

total = 0
dict={}

"""for x in range(start_year, end_year):
	for y in range(1,13):
		dict[x*100+y] = 0"""

#data = "news_db_instance.json"
data = "data/news_db_instance.json"
#data = "bd_news_dhaka_tribune.json"
with open(data, encoding="utf-8") as file:
	for line in file:
		parsed_json = json.loads(line)
		content = parsed_json["content"]
		#count = content.lower().count(key)
		date = parsed_json['date_published']['$date']
		t = parse(date)
		n = t.year*100+t.month
		# MAKE A LIST OF ALL WORD IN line
		# word_list = content.lower().split()
		if n<201701:
			word_list = TextBlob(content.lower().replace('.',' ')).words #split('#')
			# ITERATE OVER EACH WORD
			for word in word_list:
				# IF NOT EXISTS IN dict, dict[WORD] = gimmeDict()
				if word not in dict:
					dict[word] = gimmeDict()
				# INCREASE ENCOUNTER
				dict[word][n] += 1
				dict[word]["sum"] += 1
file.close()

with open('output/result.json', 'w') as fp:
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