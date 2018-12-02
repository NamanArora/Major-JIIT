import httplib, urllib, base64, json

headers = {
    # Request headers
    'api_key': '3f6ff37b63da417080ac532315a3da01',
}

station_and_codes= {}

def fun(p, q):
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
        return newdict['PeakTime'], newdict['OffPeakTime']
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def make_map(p, q):
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
	    return station_and_codes[p], station_and_codes[q]
	except Exception as e:
	    print("eghj")