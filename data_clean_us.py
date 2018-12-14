import csv

filename = "data.csv"
newfile = "newfile.csv"
stations = set()
quarters= set()
data = {}

def countRows():
	count = 0
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		csvreader.next()
		for row in csvreader:
			count = count + 1
	print(count)

def getStations():
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		csvreader.next()
		for row in csvreader:
			stations.add(row[2])
	# for station in stations:
	# 	print(station)
	# print(len(stations))	

def getQuarters():
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		csvreader.next()
		for row in csvreader:
			quarters.add(row[6])

def makeDataCompatible():
	getStations()
	getQuarters()
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		csvreader.next()
		for row in csvreader:
			if row[0] == "Weekday":
				temp = (row[0], row[2], row[3], row[5])
			else:
				temp = ("Weekend", row[2], row[3], row[5])	
			# print("yo")
			if row[2]=="Pentagon" :
    				print(row[5])
			if temp in data:
				data[temp] = data[temp] + int(row[6])
			else:
				data[temp] = int(row[6])
	fields = ['DAYSTATUS', 'ENTSTATION', 'EXTSTATION', 'QUARTER', 'AVG_TRIPS']
	with open(newfile, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(fields)
		for key, value in data.items():
			temp = list(key)
			temp.append(value)
			writer.writerow(temp)


makeDataCompatible()