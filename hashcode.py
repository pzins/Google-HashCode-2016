
import math

#global
nb_rows = 0
nb_cols = 0
nb_drones = 0
max_turns = 0
max_load = 0
nb_types = 0
prod_w = []



def dist(a,b,c,d):
	return math.ceil(math.sqrt((a-c)*(a-c)+(b-d)*(b-d)))

def dist(a,b):
	return math.ceil(math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1])))



def findWare(_drone, _wares, _type, _nb):
	dis = 2000000
	ware = _wares[0].pos
	isOk = False;
	idx = 0;
	for i in _wares:
		res = dist(_drone.pos, i.pos) 
		if res < dis and i.items[_type] >= _nb:
			dis = res
			ware = i
			isOk = True
		idx += 1
	return idx





class Drone:
	def __init__(self,id,pos):
		global nb_types

		self.id = id
		self.pos = pos
		self.items = []
		for i in range(nb_types):
			self.items.append(0)
		pass

	def load(ware,type,nb):
		global prod_w
		global max_load

		cost = dist(ware.pos,self.pos)
		if not ware.release(type,nb):
			print "############ error load ",self.id,self.ware,self.type,self.nb
		if self.weight() + nb*prod_w[type] > max_load:
			print "############ error load wieght ",self.id,self.ware,self.type,self.nb
		self.items[type] += nb
		cost += 1
		return cost

	def deliver(target,order,type,nb):
		cost = dist(target.pos,self.pos)
		if not order.get(type,nb):
			print "############ error load ",self.id,self.ware,self.type,self.nb
		cost += 1
		return cost

	def weight(self):
		global nb_types
		global prod_w

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





# print findWare([15,300], r.wares)

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