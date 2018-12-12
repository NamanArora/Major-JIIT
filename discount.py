def findDiscount(demand, fare):
	enp = -0.48
	ep = -0.24
	ex = 0.085
	rnpf = rpf = float(demand)
	ans = -1
	ff = float(fare)
	orev = ff*rnpf
	# a = fnpd/ff
	# b = fpd/fnpd
	# assuming no price hike in peak hours, 
	# we have fpd = ff
	# 	=> b = 1/a
	for d in range(1, 100):
		discount = float(d)
		fnpd = ff-(ff*discount/100)
		fpd = ff+(ff*discount/100)
		
		rnpd = rnpf*(1 + enp*((fnpd/ff)-1) + ex*((fpd/fnpd)-1))
		rpd = rpf*(1 + ep*((fpd/ff)-1) - ex*((fpd/fnpd)-1))
		
		revnpd = fnpd*rnpd
		revpd = rpd*fpd
		# print(str(revpd) + ", " + str(revnpd))
		print(str(revpd+revnpd - 2*(orev)) + " at " + str(d) + "%")