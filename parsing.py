import sys
import json
import timeit
from datetime import datetime
from dateutil.parser import parse

start = timeit.default_timer()
key = sys.argv[1]
print(key)
seq = 0
total = 0
prev_month = 0
dict = {}
for x in range(2008,2017):
	for y in range(1,13):
		dict[x*100+y] = 0
data = "data/news_db_instance.json"
#data = "bd_news_dhaka_tribune.json"
with open(data, encoding="utf-8") as file:
	for line in file:
		parsed_json = json.loads(line)
		content = parsed_json["content"]
		count = content.lower().count(key)
		date = parsed_json['date_published']['$date']
		t = parse(date)
		n = t.year*100+t.month
		if(t.year<2017): 
			dict[n] += count
			total+=count
		#print(t.year, t.month, " count: ", count)
	#x = [l.strip() for l in file]
file.close()

i = 1
for x in range(2008,2017):
	for y in range(1,13):
		print(i,":", x*100+y, dict[x*100+y])
		i+=1

stop = timeit.default_timer()
minutes = int((stop-start)/60)
seconds = int((stop-start)%60)
print("Total occurence of ", key, ": ", total)
print("runtime: ", minutes, "minutes", seconds, "seconds")
#print(stop-start)

##########################
#json: http://docs.python-guide.org/en/latest/scenarios/json/
#