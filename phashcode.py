
import math

#global
nb_rows = 0
nb_cols = 0
nb_drones = 0
max_turns = 0
max_load = 0
nb_types = 0
prod_w = []


nb_cmd = 0

def dist(a,b,c,d):
	return math.ceil(math.sqrt((a-c)*(a-c)+(b-d)*(b-d)))

def dist(a,b):
	return math.ceil(math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1])))



def findWare(_drone, _wares, _type, _nb):
	dis = 2000000
	ware = _wares[0].pos
	isOk = False;
	ware_i = 0
	idx = 0;
	for i in _wares:
		res = dist(_drone.pos, i.pos) 
		if res < dis and i.items[_type] >= _nb:
			dis = res
			ware = i
			isOk = True
			ware_i = idx
		idx += 1
	if i.items[_type] < _nb:
		print "problem find correct ware"
	return ware_i



def closerWares(_drone, _wares, _type, _nb):
	idx = 0;
	dists = []
	for i in _wares:
		dists.append([idx, dist(_drone.pos, i.pos)])
		idx += 1
	dists.sort(key=lambda x: x[1])
	return dists




class Drone:
	def __init__(self,id,pos):
		global nb_types

		self.id = id
		self.pos = pos
		self.items = []
		for i in range(nb_types):
			self.items.append(0)
		pass

	def load(self,ware,type,nb):
		global prod_w
		global max_load
		global nb_cmd

		cost = dist(ware.pos,self.pos)
		if not ware.release(type,nb):
			print "############ error load ",self.id
		if self.weight() + nb*prod_w[type] > max_load:
			print "############ error load wieght ",self.id
		self.items[type] += nb
		cost += 1
		self.pos = ware.pos

		c = cLoadUnload(self.id,'L',ware.id,type,nb)
		c.write()
		nb_cmd += 1

		return cost

	def deliver(self,order,type,nb):
		global nb_cmd

		cost = dist(order.pos,self.pos)
		if not order.get(type,nb):
			print "############ error load ",self.id,self.ware,self.type,self.nb
		cost += 1
		self.pos = order.pos

		self.items[type] = 0

		c = cDeliver(self.id,order.id,type,nb)
		c.write()
		nb_cmd += 1

		return cost

	def weight(self):
		global nb_types
		global prod_w
		w = 0
		for i in range(nb_types):
			w += prod_w[i] * self.items[i]
		return w

	def __str__(self):
		return str(self.id)+"\n"+str(self.pos)+"\n"+str(self.items)



class Ware:
	def __init__(self,id,pos,nb_prod_type):
		
		self.id = id
		self.pos = pos
		self.items = nb_prod_type

	def release(self,type,nb):
		if self.items[type]<nb:
			return False
		self.items[type]-=nb
		return True

	def giveMax(self, type):
		nb = self.items[type]
		self.items[type] = 0
		return nb

	def __str__(self):
		return str(self.id)+"\n"+str(self.pos)+"\n"+str(self.items)
	
class Order:
	def __init__(self,id,pos,nb_items,types):
		global nb_types
		#print "tyypes",types
		self.id = id
		self.pos = pos
		#self.nb_items = nb_items
		#self.types = types
		self.items = []
		for i in range(nb_types):
			self.items.append(0)
		for i in types:
			self.items[i] += 1
		#print self.items

	def get(self,type,nb):
		if self.items[type] < nb:
			return False
		self.items[type]-=1
		return True

	def isFinished(self):
		s = 0
		for i in self.items:
			s += i
		return s==0

	def next_need(self):
		global nb_types
		for i in range(nb_types):
			if self.items[i] >0:
				return i,self.items[i]


	def __str__(self):
		return str(self.id)+"\n"+str(self.pos)+"\n"+str(self.items)


class Reader:
	def __init__(self):

		self.nb_wares = 0
		self.wares = []
		self.nb_orders = 0
		self.orders = []
		self.drones = []
		

	def read(self,name):
		global nb_rows 
		global nb_cols 
		global nb_drones 
		global max_turns 
		global max_load 
		global nb_types 
		global prod_w 

		lines = []
		with open(name) as f:
			lines = f.readlines()
		linesStrip = []
		for s in lines:
			linesStrip.append(s.strip('\n'))

		#print linesStrip


		header = linesStrip[0].split()
		nb_rows 	= int(header[0])
		nb_cols 	= int(header[1])
		nb_drones 	= int(header[2])
		max_turns 	= int(header[3])
		max_load 	= int(header[4])

		#print self.nb_rows 
		#print self.nb_cols 
		#print self.nb_drones 	
		#print self.max_turns 	
		#print self.max_load 	



		nb_types = int(linesStrip[1])
		#print self.nb_types

		prod_w_str = linesStrip[2].split()
		for s in prod_w_str:
			prod_w.append(int(s))
		#print self.prod_w


		self.nb_wares = int(linesStrip[3])
		for i in range(self.nb_wares):
			pos_str = linesStrip[4+2*i].split()
			pos = (int(pos_str[0]),int(pos_str[1]))
			items = []
			items_str = linesStrip[4+2*i+1].split()
			for s in items_str:
				items.append(int(s))
			self.wares.append(Ware(i,pos,items))

		print "size of wares = = = =",str(len(self.wares))
		#for x in self.wares:
		#	print x

		index = self.nb_wares*2+4
		self.nb_orders = int(linesStrip[index])
		#print self.nb_orders
		index +=1
		for i in range(self.nb_orders):
			pos_str = linesStrip[index].split()
			index+=1
			pos = (int(pos_str[0]),int(pos_str[1]))

			nb_items = int(linesStrip[index])
			index +=1

			types = []
			types_str = linesStrip[index].split()
			index+=1
			for s in types_str:
				types.append(int(s))

			self.orders.append(Order(i,pos,nb_items,types))



		#for x in self.orders:
		#		print x

		for i in range(nb_drones):
			id = i
			pos = self.wares[0].pos
			self.drones.append(Drone(id,pos))
			#print self.drones[i]


		



	def commander(self):
		global nb_drones
		drone_to_order = []
		for i in range(nb_drones):
			drone_to_order.append([])
		di = 0
		#print "nb_order ====",self.nb_orders
		for i in range(self.nb_orders):
			drone_to_order[di].append(i)
			di += 1
			if di == nb_drones:
				di = 0
		# print drone_to_order
		#repartition des X orders sur les Y drones
		#drone_to_order: tab de liste d'order

		for j in range(self.nb_orders):
			for di in range(nb_drones):
				drone = self.drones[di]
				if(len(drone_to_order[di]) <= j):
					continue
				order = self.orders[drone_to_order[di][j]]

				#si l'order est deja fini on enleve de la liste des order pr ce drone la
				if order.isFinished():
					drone_to_order[di].pop()
					continue


				type_need,nb_need = order.next_need()
				listWares = closerWares(drone, self.wares, type_need, nb_need)

				ware_id = findWare(drone,self.wares,type_need,nb_need)
				ware = self.wares[ware_id]
				if not ware.release(type_need, nb_need):
					listWares = closerWares(drone, self.wares, type_need, nb_need)
					get = 0
					idx = 0
					while nb_need < get:
						war = self.wares[listWares[idx][0]]
						get += war.giveMax(type_need)
						if drone.weight() + nb_need*prod_w[type_need] > max_load:
							for i in range(nb_need):
								drone.load(war,type_need,1)
								drone.deliver(order,type_need,1)
						else:
							drone.load(war,type_need,nb_need)
							drone.deliver(order,type_need,nb_need)
						idx += 1
				else:
					if drone.weight() + nb_need*prod_w[type_need] > max_load:
						for i in range(nb_need):
							drone.load(ware,type_need,1)
							drone.deliver(order,type_need,1)
					else:
						drone.load(ware,type_need,nb_need)
						drone.deliver(order,type_need,nb_need)




class cLoadUnload:
	def __init__(self, _drone, _tag, _ware, _prod, _nb):
		self.drone = _drone
		self.tag = _tag
		self.ware = _ware
		self.prod = _prod
		self.nb = _nb
	def write(self):
		st = str(self.drone) + " " + str(self.tag) + " " + str(self.ware) + " " + str(self.prod) +  "  " + str(self.nb) + "\n"
		file.write(st)

class cDeliver:
	def __init__(self, _drone, _order, _prod, _nb):
		self.drone = _drone
		self.order = _order
		self.prod = _prod
		self.nb  =_nb
	def write(self):
		st = str(self.drone) + " D " + str(self.order) + " " + str(self.prod) +  "  " + str(self.nb) + "\n"
		file.write(st)

class cWait:
	def __init__(self, _drone, _w):
		self.drone = _drone
		self.wait = _w
	
	def write(self):
		st = str(self.drone) + " W " + str(self.wait) + "\n"
		file.write(st)	

filename = "redundancy.in"
filename = "busy_day.in"
filename = "mother_of_all_warehouses.in"
		

r = Reader()
r.read(filename)
#r.read("busy_day.in")


file = open("solution_"+filename+".txt", "w")

r.commander()
print "max load" + str(max_load) + "  " + str(prod_w[49])



#com = cWait(0,10)
#com.write()




# print findWare([15,300], r.wares)




















print "---------------"

# print "-------++--------"
# print r.orders[0]

	# def start(self):
	# 	cost = 0
	# 	o = self.orders[0]
	# 	d = self.drones[0]
	# 	print d


	# 	w = findWare(d, self.wares)
	# 	d.pos = w[2]
	# 	d.load(self.wares[w[0]]
