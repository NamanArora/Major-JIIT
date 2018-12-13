import httplib, urllib, base64, json
import csv
import pandas as pd

headers = {
    # Request headers
    'api_key': '3f6ff37b63da417080ac532315a3da01',
}

station_and_codes = {}
faulty_data = []

def getPricesFromPtoQ(p, q):
    params = urllib.urlencode({
        'FromStationCode': p,
        'ToStationCode': q,
    })
    fares = {}
    try:
        conn = httplib.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/Rail.svc/json/jSrcStationToDstStationInfo?%s" % params, "", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        # print(data)
        j = json.loads(data)
        x = j['StationToStationInfos']
        z = x[0]
        y = z['RailFare']
        # print(y)
        newdict = dict((k.encode('ascii'), v) for (k, v) in y.items())
        # print("new value= ")
        # print(newdict['PeakTime'])
        value = float(newdict['PeakTime'])
        # print(type(value))
        return value# , newdict['OffPeakTime']
    except Exception as e:
        print(e)

def makeNameToCodeMap():
	params = urllib.urlencode({
	    # Request parameters
	    # 'LineCode': '',
	})
	try:
	    conn = httplib.HTTPSConnection('api.wmata.com')
	    conn.request("GET", "/Rail.svc/json/jStations?%s" % params, "", headers)
	    response = conn.getresponse()
	    data = response.read()
	    # print(data)
	    conn.close()
	    j = json.loads(data)
	    stations = j['Stations']
	    for station in stations:
	        # print(station['Name'])
	        station_and_codes[station['Name']] = station['Code']
	        # print(station['Name'] + ", " + station['Code'])
	    # print(station_and_codes)    
	    # for x in station_and_codes:
	    #     print(x + " " + station_and_codes[x] + "\n")
	    # keys = station_and_codes.keys()    
	    # print("printing fares from " + keys[0] + " to " + keys[1] + " ")
	    # fun(station_and_codes.get(keys[0]), station_and_codes.get(keys[1]))
	    # print(len(station_and_codes))
	    # print("stations from api are\n")
	    # print(station_and_codes.keys())
	    return station_and_codes
	except Exception as e:
	    print("eghj")

def makeNameToCodeMapFromFile():
	filename = "newfile.csv"
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		csvreader.next()
		for row in csvreader:
			station_and_codes[row[1]] = 1
	# print("stations in newfile\n")
	# print(station_and_codes.keys())		

def addPricesToCSV():
	fields = ['ENTSTATION', 'EXTSTATION', 'Fare']
	filename = "prices.csv"
	srcctr = ctr = 1
	makeNameToCodeMap()
	with open(filename, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(fields)
		stations = station_and_codes.keys()
		for src in stations:
			dstctr = 1
			for dst in stations:
				if(src==dst):
					continue
				temp = []
				fare = getPricesFromPtoQ(station_and_codes[src], station_and_codes[dst])
				temp.append(src)
				temp.append(dst)
				temp.append(fare)
				writer.writerow(temp)
				print(str(ctr) + " " + str(srcctr) + " " + str(dstctr) + " " + str(temp))
				ctr = ctr + 1
				dstctr = dstctr + 1

def readPrices():
	filename = "prices.csv"
	prices = {}
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		csvreader.next()
		for row in csvreader:
			prices[(row[0], row[1])] = float(row[2])
	return prices

def checkInTable():
	makeNameToCodeMapFromFile()
	keys1 = station_and_codes.keys()
	# for k in keys1:
	# 	print(k)
	# print("########################################################################")	
	makeNameToCodeMap()
	keys2 = station_and_codes.keys()
	# for k in keys:
	# 	print(k)
	keys1.sort()
	keys2.sort()
	# for i in range(0, len(keys1)):
	# 	# if
	# 	print(keys1[i] + "\t\t\t\t\t\t\t\t" + keys2[i])
	for i in range(0, len(keys1)):
		if keys1[i] in keys2:
			keys2.remove(keys1[i])
	print(keys2)
	print(len(keys2))

def read_faulty_data():
	filename = "newfile.csv"
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		csvreader.next()
		for row in csvreader:
			faulty_data.append(row)

def write_faulty_data():
	filename = "newfile.csv"
	fields = ['DAYSTATUS', 'ENTSTATION', 'EXTSTATION', 'QUARTER', 'AVG_TRIPS']
	with open(filename, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(fields)
		for row in faulty_data:
			writer.writerow(row)


def updatePtoQInNewFile(p, q):
		for row in faulty_data:
			if row[1] == p:
				row[1] = q
			if row[2] == p:
				row[2] = q;

# checkInTable()
read_faulty_data()

updatePtoQInNewFile("Addison Road", "Addison Road-Seat Pleasant")
updatePtoQInNewFile("Archives-Navy Memorial", "Archives-Navy Memorial-Penn Quarter")
updatePtoQInNewFile("Ballston", "Ballston-MU")
updatePtoQInNewFile("Branch Avenue", "Branch Ave")
updatePtoQInNewFile("Brookland", "Brookland-CUA")
updatePtoQInNewFile("College Park-U of MD", "College Park-U of Md")
updatePtoQInNewFile("Dunn Loring", "Dunn Loring-Merrifield")
updatePtoQInNewFile("Foggy Bottom", "Foggy Bottom-GWU")
updatePtoQInNewFile("Gallery Place-Chinatown", "Gallery Pl-Chinatown")
updatePtoQInNewFile("Georgia Avenue-Petworth", "Georgia Ave-Petworth")
updatePtoQInNewFile("Grosvenor", "Grosvenor-Strathmore")
updatePtoQInNewFile("King Street", "King St-Old Town")
updatePtoQInNewFile("Minnesota Avenue", "Minnesota Ave")
updatePtoQInNewFile("Morgan Blvd.", "Morgan Boulevard")
updatePtoQInNewFile("Mt. Vernon Square-UDC", "Mt Vernon Sq 7th St-Convention Center")
updatePtoQInNewFile("Navy Yard", "Navy Yard-Ballpark")
updatePtoQInNewFile("Gallaudet'Friendship Heights", "NoMa-Gallaudet U")
updatePtoQInNewFile("Potomac Avenue", "Potomac Ave")
updatePtoQInNewFile("Rhode Island Avenue", "Rhode Island Ave-Brentwood")
updatePtoQInNewFile("Reagan Washington National Airport", "Ronald Reagan Washington National Airport")
updatePtoQInNewFile("Shaw-Howard University", "Shaw-Howard U")
updatePtoQInNewFile("U Street-Cardozo", "U Street/African-Amer Civil War Memorial/Cardozo")
updatePtoQInNewFile("Vienna", "Vienna/Fairfax-GMU")
updatePtoQInNewFile("West Falls Church", "West Falls Church-VT/UVA")
updatePtoQInNewFile("Wiehle", "Wiehle-Reston East")
updatePtoQInNewFile("Woodley Park-Zoo", "Woodley Park-Zoo/Adams Morgan")

write_faulty_data()