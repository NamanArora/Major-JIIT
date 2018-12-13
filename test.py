from discount import findDiscount
import matplotlib.pyplot as plt 
import csv
import plotly.plotly as py
import plotly.graph_objs as go


def netrevVsDpPlot():
	netrev = findDiscount(25, 10)
	d = [i for i in range(1, 31)]

	plt.plot(d, netrev)
	plt.ylabel('net revenue')
	plt.xlabel('differential rate')
	plt.title('net revenue vs differential rate at demand = 25 and fare = $10')

	plt.show()

def weekdayRidershipPlot():
	filename = "newfile.csv"
	ridership = []
	quarter = []
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		csvreader.next()
		temp = {}
		for row in csvreader:
			if(row[0]=="Weekend" and row[1]=="Pentagon" or row[2]=="Pentagon"):
				if row[3] in temp:
					temp[row[3]] = temp[row[3]] + int(row[4])
				else:
					temp[row[3]] = int(row[4])	
	quarter = temp.keys()
	ridership = temp.values()
	plt.scatter(quarter, ridership)
	# plt.plot(quarter, ridership)
	plt.ylabel('ridership')
	plt.xlabel('quarter')
	plt.title('ridership vs quarter at src = Pentagon and on a weekday')

	plt.show()
	print(len(ridership))
	print(len(quarter))
		# trace = {"x":quarter,
		# "y":ridership,
		# "marker":{"color":"blue", "size":8},
		# "mode":"markers",
		# "name":"plot",
		# "type":"scatter"}
		# data = [trace]
		# layout={"title":"plot",
		# "xaxis":{"title":"quarters",},
		# "yaxis":{"title":"riderships"}
		# }
		# fig = go.Figure(data = data, layout = layout)
		# py.iplot(fig, filename="weekday-ridership")	

weekdayRidershipPlot()	