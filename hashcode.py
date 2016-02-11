class Reader:
	def __init__(self):
		self.nb_rows = 0
		self.nb_cols = 0
		self.nb_drones = 0
		self.max_turns = 0
		self.max_load = 0
		self.prod_w = []
		self.nb_wares = 0
		self.wares = []
		self.nb_orders = 0
		self.orders = []
		pass

	def read(self,name):
		lines = []
		with open(name) as f:
			lines = f.readlines()
		linesStrip = []
		for s in lines:
			linesStrip.append(s.strip('\n'))

		#print linesStrip


		header = linesStrip[0].split()
		self.nb_rows 	= int(header[0])
		self.nb_cols 	= int(header[1])
		self.nb_drones 	= int(header[2])
		self.max_turns 	= int(header[3])
		self.max_load 	= int(header[4])

		print self.nb_rows 
		print self.nb_cols 
		print self.nb_drones 	
		print self.max_turns 	
		print self.max_load 	



		self.nb_prod = int(linesStrip[1])
		print self.nb_prod

		prod_w_str = linesStrip[2].split()
		for s in prod_w_str:
			self.prod_w.append(int(s))
		print self.prod_w


		self.nb_wares = int(linesStrip[3])
		for i in range(self.nb_wares):
			dico = {}
			pos_str = linesStrip[4+2*i].split()
			#print pos_str
			dico["pos"] = (int(pos_str[0]),int(pos_str[1]))
			dico["items"] = []
			items_str = linesStrip[4+2*i+1].split()
			for s in items_str:
				dico["items"].append(int(s))

			self.wares.append(dico)


		print self.wares

		index = self.nb_wares*2+4
		self.nb_orders = int(linesStrip[index])
		print self.nb_orders
		index +=1
		for i in range(self.nb_orders):
			dico = {}
			pos_str = linesStrip[index].split()
			index+=1
			dico["pos"] = (int(pos_str[0]),int(pos_str[1]))

			dico["nb_items"] = int(linesStrip[index])
			index +=1

			dico["types"] = []
			types_str = linesStrip[index].split()
			index+=1
			for s in types_str:
				dico["types"].append(int(s))
			self.orders.append(dico)

file = open("solution.txt", "w")


class cLoadUnload:
	def __init__(self, _drone, _tag, _ware, _prod, _nb):
		self.drone = _drone
		self.tag = _tag
		self.ware = _ware
		self.prod = _prod
		self.nb = _nb
	def write(self):
		st = str(self.drone) + " " + str(self.tag) + " " + str(self.ware) + " " + str(self.prod) +  "  " + str(self.nb)
		file.write(st)

class cDeliver:
	def __init__(self, _drone, _order, _prod, _nb):
		self.drone = _drone
		self.order = _order
		self.prod = _prod
		self.nb  =_nb
	def write(self):
		st = str(self.drone) + " D " + str(self.order) + " " + str(self.prod) +  "  " + str(self.nb)
		file.write(st)

class cWait:
	def __init__(self, _drone, _w):
		self.drone = _drone
		self.wait = _w
	
	def write(self):
		st = str(self.drone) + " W " + str(self.wait)
		file.write(st)	

		

r = Reader()
r.read("busy_day.in")
print "----------------------------------------"
print r.wares[0]


com = cWait(0,10)
com.write()