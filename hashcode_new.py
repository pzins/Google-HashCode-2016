import copy
import math

nb_rows = 0
nb_cols = 0
max_turns = 0
max_load = 0

nb_prod = 0
weight = []

nb_wares = 0
wares = []

nb_orders = 0
orders = []

nb_drones = 0
drones = []



def dist(a,b,c,d):
	return math.ceil(math.sqrt((a-c)*(a-c)+(b-d)*(b-d)))

def dist(a,b):
	return math.ceil(math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1])))


def closerWare(_drone, _prod, _nb):
	distMap = []
	counter = 0
	for i in wares:
		tmp = [counter, dist(_drone.pos, i.pos)]
		distMap.append(tmp)
		counter += 1
	distMap.sort(key=lambda x: x[1])
	returnMap = [x for x in distMap if wares[x[0]].items[_prod] >= _nb]

	if len(returnMap) == 0:
		print "Error : no more product ", _prod, " in wares"	
	return returnMap


class Drone:
	def __init__(self,id,pos):
		global nb_prod

		self.id = id
		self.pos = pos
		self.items = []
		for i in range(nb_prod):
			self.items.append(0)
		pass

	def load(self,ware,type,nb):
		global weight
		global max_load

		if not self.isWeightOk(type, nb):
			print "Problem weight"

		if ware.release(type,nb):
			self.items[type] += nb
			self.pos = ware.pos
			writeLoad(self.id, ware.id, type, nb)
		else:
			print "problem ware release"

	#check if drone weight is OK if we give it nb more products type
	def isWeightOk(self, type, nb):
		global weight
		global max_load
		self.items[type] += nb;
		res = True
		if self.weight() > max_load:
			res = False
		self.items[type] -= nb;
		return res


	def deliver(self,order,type,nb):
		if order.get(type,nb):
			self.pos = order.pos
			self.items[type] = 0
			writeDeliver(self.id, order.id, type, nb)
		

	#return drone weight
	def weight(self):
		global nb_prod
		global weight
		w = 0
		for i in range(nb_prod):
			w += weight[i] * self.items[i]
		return w

	def __str__(self):
		return str(self.id)+"\n"+str(self.pos)+"\n"+str(self.items)



class Ware:
	def __init__(self,id,pos,nb_prod_type):
		self.id = id
		self.pos = pos
		self.items = nb_prod_type

	#give nb product type return false if not possible
	def release(self,type,nb):
		if self.items[type]<nb:
			print "Ware ", self.id, "cannot give ", nb, " product ", type
			return False
		self.items[type]-=nb
		return True


	#a voir
	def giveMax(self, type):
		nb = self.items[type]
		self.items[type] = 0
		return nb

	def hasEnough(self, prod, nb):
		return self.items[prod] >= nb

	def __str__(self):
		return str(self.id)+"\n"+str(self.pos)+"\n"+str(self.items)
	
class Order:
	def __init__(self,id,pos,nb_items,types):
		global nb_prod
		self.id = id
		self.pos = pos
		self.items = []
		for i in range(nb_prod):
			self.items.append(0)
		for i in types:
			self.items[i] += 1

	#give nb product type to order return false if give too many products
	def get(self,type,nb):
		if self.items[type] < nb:
			print "Order ", self.id, " receives too many : ", nb, " products ", type
			return False
		self.items[type]-=nb
		return True

	#return True if order is completed
	def isFinished(self):
		s = 0
		for i in self.items:
			s += i
		return s==0

	#return next need : product type, nb
	def next_need(self):
		global nb_prod
		for i in range(nb_prod):
			if self.items[i] >0:
				if self.items[i]  * weight[i] <= max_load:
					return i,self.items[i]
				elif self.items[i]-1  * weight[i] <= max_load:
					return i, self.items[i]-1
				else:
					return i, 1
		return -1,-1


	def getNeedList(self, prod, nb):
		returnMap = []
		for i in range(nb_prod):
			if self.items[i] > 0 and prod == i and nb < self.items[i]:
				returnMap.append([i, self.items[i]-nb])
			elif self.items[i] > 0 and prod != i:
				returnMap.append([i, self.items[i]])
		return returnMap


	def nbProdNeeded(self):
		res = 0
		for i in items:
			if i > 0:
				res += 1
		return res

	def __str__(self):
		return str(self.id)+"\n"+str(self.pos)+"\n"+str(self.items)


#find closest couple drone-ware for _nb _prod
#return [id_ware, dist_drone_ware, id_drone]
def bestDrone(_prod, _nb):
	drone_dist = []
	for i in drones:
		tmp = closerWare(i, _prod, _nb)
		if len(tmp) != 0:
			tmp = tmp[0]
			tmp.append(i.id)
			drone_dist.append(tmp)
	drone_dist.sort(key=lambda x: x[1])
	if len(drone_dist) > 0:
		return drone_dist[0]
	else:
		return False



def getWare(pos, prod, nb):
	listWaresOk = []
	for w in wares:
		if w.items[prod] >= nb:
			listWaresOk.append([w.id, dist(pos, w.pos)])
	listWaresOk.sort(key=lambda x: x[1])
	return listWaresOk


def bestCompletion(_weight, prods):
	res = 10000
	sol = [-1,-1]
	for i in prods:
		for j in range(1,i[1]+1):
			tmp = max_load - _weight - weight[i[0]] * j
			if tmp > 0 and tmp < res:
				res = tmp
				sol = [i[0], j]
	return sol

def bestCompletion2(_weight, prods):


def simulate():
	stack_drones = copy.copy(drones)

	for order in orders:
		prod, nb = order.next_need()
		while prod != -1:
			if len(stack_drones) <= 0:
				stack_drones = copy.copy(drones)
			drone = stack_drones.pop(0)
			ware = wares[closerWare(drone, prod, nb)[0][0]]
			
			loadList = []
			loadList.append([prod, nb, ware.id])
			loadVal = nb * weight[prod]
			nextProdList = order.getNeedList(prod, nb)
			bestNext = bestCompletion(loadVal, nextProdList)
			if bestNext[0] != -1:
				loadList.append([bestNext[0], bestNext[1], getWare(ware.pos, bestNext[0], bestNext[1])[0][0]])
			for p in nextProdList:
				if loadVal + weight[p[0]] * p[1] <= max_load:
					loadVal += weight[p[0]] * p[1]
					loadList.append([p[0], p[1], getWare(ware.pos, p[0], p[1])[0][0]])

			for l in loadList:
				drone.load(wares[l[2]], l[0], l[1])

			for l in loadList:
				drone.deliver(order, l[0], l[1])
			prod, nb = order.next_need()





#BEST BEST BEST
# def simulate():
# 	stack_drones = copy.copy(drones)

# 	for order in orders:
# 		prod, nb = order.next_need()
# 		while prod != -1:
# 			if len(stack_drones) <= 0:
# 				stack_drones = copy.copy(drones)
# 			drone = stack_drones.pop(0)
# 			ware = wares[closerWare(drone, prod, nb)[0][0]]
			
# 			loadList = []
# 			loadList.append([prod, nb])
# 			loadVal = nb * weight[prod]
# 			nextProdList = order.getNeedList(prod, nb)
# 			for p in nextProdList:
# 				if loadVal + weight[p[0]] * p[1] <= max_load and ware.hasEnough(p[0], p[1]):
# 					loadVal += weight[p[0]] * p[1]
# 					loadList.append([p[0], p[1]])
# 			for l in loadList:
# 				drone.load(ware, l[0], l[1])

# 			for l in loadList:
# 				drone.deliver(order, l[0], l[1])
# 			prod, nb = order.next_need()




# def simulate():
# 	stack_drones = copy.copy(drones)

# 	for order in orders:
# 		prod, nb = order.next_need()
# 		while prod != -1:
# 			if len(stack_drones) <= 0:
# 				stack_drones = copy.copy(drones)
# 			drone = stack_drones.pop(0)
# 			ware = wares[closerWare(drone, prod, nb)[0][0]]
# 			drone.load(ware, prod, nb)
# 			drone.deliver(order, prod, nb)
# 			prod, nb = order.next_need()
				




def start():
	global nb_drones

	for j in range(nb_orders):
		for i in range(nb_prod):
			nb = orders[j].items[i]
			if nb > 0:
				if nb * weight[i] < max_load:
			#		print "ORDERS :", j, "; PROD :", i, "; NB :", nb
					res = bestDrone(i, nb)
			#		print "WARE :", res[0], "; DIST :", res[1], "; DRONE :", res[2]
					drone = drones[res[2]]
					ware = wares[res[0]]
					drone.load(wares[res[0]], i, nb)
					drone.deliver(orders[j], i, nb)
				else:
					for it in range(nb):
						res = bestDrone(i, 1)
						drone = drones[res[2]]
						ware = wares[res[0]]
						drone.load(wares[res[0]], i, 1)
						drone.deliver(orders[j], i, 1)
		#raw_input()


def writeLoad(_drone, _ware, _prod, _nb):
	global file
	st = str(_drone) + " L " + str(_ware) + " " + str(_prod) +  "  " + str(_nb) + "\n"
	file.write(st)

def writeUnload(_drone, _ware, _prod, _nb):
	global file
	st = str(_drone) + " U " + str(_ware) + " " + str(_prod) +  "  " + str(_nb) + "\n"
	file.write(st)

def writeDeliver(_drone, _order, _prod, _nb):
	global file
	st = str(_drone) + " D " + str(_order) + " " + str(_prod) +  "  " + str(_nb) + "\n"
	file.write(st)

def writeWait(_drone, _wait):
	global file
	st = str(_drone) + " W " + str(_wait) + "\n"
	file.write(st)
	

class Reader:

	def read(self,name):
		global nb_rows 
		global nb_cols 
		global nb_drones 
		global max_turns 
		global max_load 
		global nb_prod 
		global weight 
		global nb_wares
		global wares
		global nb_orders
		global orders
		global drones

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

		#print nb_rows 
		#print nb_cols 
		#print nb_drones 	
		#print max_turns 	
		#print max_load 	



		nb_prod = int(linesStrip[1])
		#print nb_prod

		weight_str = linesStrip[2].split()
		for s in weight_str:
			weight.append(int(s))
		#print weight


		nb_wares = int(linesStrip[3])
		for i in range(nb_wares):
			pos_str = linesStrip[4+2*i].split()
			pos = (int(pos_str[0]),int(pos_str[1]))
			items = []
			items_str = linesStrip[4+2*i+1].split()
			for s in items_str:
				items.append(int(s))
			wares.append(Ware(i,pos,items))

		index = nb_wares*2+4
		nb_orders = int(linesStrip[index])
		#print nb_orders
		index +=1
		for i in range(nb_orders):
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

			orders.append(Order(i,pos,nb_items,types))

		for i in range(nb_drones):
			id = i
			pos = wares[0].pos
			drones.append(Drone(id,pos))

filename = "mother_of_all_warehouses.in"
filename = "busy_day.in"
filename = "redundancy.in"
		

r = Reader()
r.read(filename)


file = open("solution_"+filename+".txt", "w")
simulate()
# start()













