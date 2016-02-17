import numpy as np
import math

nb_rows, nb_cols, nb_drones, nb_wares, nb_orders, nb_types, max_tursn, max_load	= 0,0,0,0,0,0,0,0
wares,orders,prod_weight, prod_weight_sorted, drones = [],[],[], [],[]


def write_load( drone, ware, prod, nb):
	st = str(drone) + " L " + str(ware) + " " + str(prod) +  " " + str(nb) + "\n"
	file_out.write(st)

def write_deliver(drone,order, prod,nb):
	st = str(drone) + " D " + str(order) + " " + str(prod) +  " " + str(nb) + "\n"
	file_out.write(st)



def dist(a,b,c,d):
	return int(math.ceil(math.sqrt((a-c)*(a-c)+(b-d)*(b-d))))

def dist(a,b):
	return int(math.ceil(math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))))


def sort_according_to_weight(tab):
	change = True
	while change:
		change = False
		for i in range(len(tab)-1):
			if prod_weight[tab[i]] < prod_weight[tab[i+1]]:
				temp = tab[i]
				tab[i] = tab[i+1]
				tab[i+1] = temp
				chage = True



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
			print "############ error load ",self.id,ware,type,nb
		if self.weight() + nb*prod_w[type] > max_load:
			print "############ error load wieght ",self.id,ware,type,nb
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
			print "############ error load ",self.id,ware,type,nb
		cost += 1
		self.pos = order.pos

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




class Batch():

	def __init__(self,pos):
		self.pos = pos
		self.targets_used = []
		"""self.targets= []
		for i in range(nb_orders):
			self.targets.append([])
			for j in range(nb_types):
				self.targets[i].append(0)"""
		self.weight = 0

		self.targets2 = {}


	def add(self,target,type,nb):
		"""print "btach try add "+str(nb)+" * type "+str(type)
		if self.weight + nb * prod_weight[type] > max_load:
			print "########### ERRORR ##########"
			return False
		if target not in self.targets_used:
			self.targets_used.append(target)
		self.targets[target][type] += nb
		self.weight += prod_weight[type] * nb
		return True"""

		if self.weight + nb * prod_weight[type] > max_load:
			#print "########### ERRORR ########## actual weight "+str(self.weight)+" max_load = "+str(max_load)
			return False
		if target not in self.targets2.keys():
			self.targets2[target] = {}
			self.targets_used.append(target)
		if type not in self.targets2[target].keys():
			self.targets2[target][type] = 0
		self.targets2[target][type]  += nb
		self.weight += prod_weight[type] * nb
		return True

	def ordonner(self,drone,ware):
		""" ordonne les livraisons """
		"""while len(self.targets_used) > 0 :
			dist_to_targets = []
			for idx in self.targets:
				dist_to_targets.append(dist(self.pos,orders[idx].pos))
			nearest = np.argmin(np.array(dist_to_targets))
			t = self.targets[nearest]
			for i in range(nb_types):
				if self.targets[t][i] > 0:
					print "# WRITE DELIVER t self.targets[t][i] if i"
			self.targets_used.remove(t)"""
		#print "###### ordonner #############"
		#print self.targets2.keys()
		#LOAD
		for target in self.targets2.keys():
			#print self.targets2[target].keys()
			for t in self.targets2[target].keys():
				write_load(drone,ware,t,self.targets2[target][t])


		# DELIVER
		#self.pos = drones[drone].pos
		while len(self.targets_used) > 0 :
			#print "target_use = ",self.targets_used
			dist_to_targets = []
			for idx in self.targets_used:
				dist_to_targets.append(dist(self.pos,orders[idx].pos))
			nearest = np.argmin(np.array(dist_to_targets))
			target = self.targets_used[nearest]
			for k in self.targets2[target].keys():
				write_deliver(drone,target,k,self.targets2[target][k])
				#print "# WRITE DELIVER target self.targets[target][k]"
			self.pos = orders[target].pos
			self.targets_used.remove(target)

		#print "---------------------------------------"






class Ware:
	def __init__(self,id,pos,nb_items_of_type):
		self.id = id
		self.pos = pos
		self.items = nb_items_of_type
		self.batches = []
		self.assigned_drones = []


	def initialize_targets(self):
		self.targets_used = []
		self.targets= []
		self.targets2 = []
		for i in range(nb_orders):
			self.targets.append([])
			self.targets2.append([])
			for j in range(nb_types):
				self.targets[i].append(0)

		#print self.targets
		#i = input()


	def release(self,type,nb):
		if self.items[type]<nb:
			return False
		self.items[type]-=nb
		return True

	def __str__(self):
		return str(self.id)+"\n"+str(self.pos)+"\n"+str(self.items)

	def sort_targets2(self):
		""" sort targets2 by weight """
		for i in self.targets_used:
			sort_according_to_weight(self.targets2[i])


	def create_batches(self):
		""" create batches """
		batch = Batch(self.pos)
		t = self.targets_used.pop(0)
		#print self.targets_used
		#print len(self.targets_used)
		for aa in range(50000): #while 1:	
			#print aa	
			##print self.targets2[t]	
			#i = input()
			if len(self.targets2[t]) <= 0:
				##print "empty targets2[t]"
				##print "targets_used = ",self.targets_used
				if len(self.targets_used) <= 0:
					#print "////////////// BREAK ///////////////////"
					self.batches.append(batch)
					break
				else:
					t = self.targets_used.pop(0)
					##print "new t = ",t

			if len(self.targets2[t]) == 0:
				##print "new t empyt !!!!!!!!!!!!!!!!!"
				continue
			##print self.targets2[t]	
			test = self.targets2[t][0]						
			if batch.add(t,test,1):
				self.targets2[t].pop(0)
			else:
				self.batches.append(batch)
				batch = Batch(self.pos)
		#print "created batches = ",len(self.batches)
	

	def create_batches2(self):
		for target in self.targets_used:
			batch = Batch(self.pos)
			for t in self.targets2[target]:
				if batch.add(target,t,1) == False:
					self.batches.append(batch)
					batch = Batch(self.pos)
			if batch.weight >0:
				self.batches.append(batch)


	def start(self):
		print "nb batches = ",len(self.batches)
		nb_drones_assigned = len(self.assigned_drones)


		"""nb_batch_per_drone = int( float(len(self.batches))/nb_drones_assigned)

		index = 0
		for i in range(nb_drones_assigned):
			for b in range(nb_batch_per_drone):
				drone = self.assigned_drones[i]
				self.batches[index].ordonner(drone,self.id)
				index += 1
"""
		drone_index = 0
		drone = self.assigned_drones[drone_index]
		for batch in self.batches:
			drone = self.assigned_drones[drone_index]
			batch.ordonner(drone,self.id)
			drone_index += 1
			if drone_index == nb_drones_assigned:
				drone_index = 0


	def validate_needs(self):
		for i in self.targets_used:
			from_wares = self.targets2[i]
			needed =  orders[i].types
			for x in from_wares:
				if x not in needed:
					print "ERROR###############################",x
					print from_wares
					print needed
					i = input()
			


class Order:
	def __init__(self,id,pos,nb_items,types):
		print "nb_types = ",nb_types
		self.id = id
		self.pos = pos
		self.items = []
		self.types = types
		for i in range(nb_types):
			self.items.append(0)
		for i in types:
			self.items[i] += 1

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





def read(filename):
	global nb_rows, nb_cols, nb_drones, nb_wares, nb_orders, nb_types, max_tursn, max_load
	global wares,orders,prod_weight,prod_weight_sorted

	lines = []
	with open(filename) as f:
		lines = f.readlines()


	header = lines[0].split()
	nb_rows 	= int(header[0])
	nb_cols 	= int(header[1])
	nb_drones 	= int(header[2])
	max_turns 	= int(header[3])
	max_load 	= int(header[4])

	nb_types = int(lines[1])

	prod_weight_str = lines[2].split()
	for s in prod_weight_str:
		prod_weight.append(int(s))

	temp = np.array(prod_weight)
	print np.argsort(temp)
	prod_weight_sorted = np.argsort(temp)[::-1]
	print prod_weight_sorted


	nb_wares = int(lines[3])
	for i in range(nb_wares):
		pos_str = lines[4+2*i].split()
		pos = (int(pos_str[0]),int(pos_str[1]))
		items = []
		items_str = lines[4+2*i+1].split()
		for s in items_str:
			items.append(int(s))
		wares.append(Ware(i,pos,items))

	index = 4+2*nb_wares
	nb_orders = int(lines[index])
	index += 1

	for i in range(nb_orders):
		pos_str = lines[index].split()
		index +=1
		pos = (int(pos_str[0]),int(pos_str[1]))
		nb_items = int(lines[index])
		index+=1

		types = []
		types_str = lines[index].split()
		index+=1
		for s in types_str:
			types.append(int(s))
		orders.append(Order(i,pos,nb_items,types))



	for i in range(nb_drones):
		drones.append(Drone(i,wares[0].pos))








filename = "busy_day.in"
#filename = "mother_of_all_warehouses.in"
#filename = "redundancy.in"


read(filename)

file_out = open("solution_"+filename+".txt", "w")


print nb_orders
print nb_drones
print nb_wares
print nb_rows
print nb_cols
print max_load
print prod_weight
#
#for i in wares:
#	print i
#for j in orders:
#	print j
#
#

for w in wares:
	w.initialize_targets()


dist_order_to_ware = np.zeros((nb_orders,nb_wares))
for o in range(nb_orders):
	for w in range(nb_wares):
		dist_order_to_ware[o][w] = dist(orders[o].pos,wares[w].pos)


print dist_order_to_ware
print np.shape(dist_order_to_ware)

nearest_wares = np.argsort(dist_order_to_ware)
print nearest_wares
# type 0

for prod_type in range(nb_types):
	for pref in range(nb_wares):
		for i in range(nb_orders):
			need = orders[i].items[prod_type]
			if need == 0 :
				continue
			ware_idx = nearest_wares[i][pref]
			available = wares[ware_idx].items[prod_type]
			if available == 0:
				continue
			#print need,available
			if need <= available:
				orders[i].items[prod_type] -= need
				wares[ware_idx].items[prod_type] -= need
				#print "order "+str(i)+ " takes "+str(need)+" from ware "+str(ware_idx)
				if i not in wares[ware_idx].targets_used:
					wares[ware_idx].targets_used.append(i)
				# not used wares[ware_idx].targets[i][prod_type] += need
				for a in range(need):
					wares[ware_idx].targets2[i].append(prod_type)
			else:
				orders[i].items[prod_type] -= available
				wares[ware_idx].items[prod_type] -= available
				#print "order "+str(i)+ " takes "+str(available)+" from ware "+str(ware_idx)
				if i not in wares[ware_idx].targets_used:
					wares[ware_idx].targets_used.append(i)
				#not used wares[ware_idx].targets[i][prod_type] += available
				for a in range(available):
					wares[ware_idx].targets2[i].append(prod_type)


print "end of repartition"

nb_batches = np.zeros((nb_wares))
total_batches = 0
index = 0

#TEST
"""empty = 0
for i in wares[0].targets2:
	if len(i) == 0:
		empty += 1
print empty
print nb_orders - len(wares[0].targets_used)

i = input()"""
##########################""



for w in wares:
	w.sort_targets2()
	w.validate_needs()
	##print len(w.targets_used)
	w.create_batches2()
	nb_batches[index] = float(len(w.batches))
	total_batches += nb_batches[index]
	index+=1

allocated_drones = np.floor((nb_batches/total_batches)*nb_drones)

allocated_drones = np.maximum(allocated_drones,1)

print allocated_drones
nb_allocated_drones = int(np.sum(allocated_drones))

print nb_allocated_drones

print nb_drones

biggest_wares = np.argsort(allocated_drones)[::-1]
print biggest_wares

if nb_drones-nb_allocated_drones>0:
	for i in range(nb_drones-nb_allocated_drones):
		allocated_drones[biggest_wares[i]] += 1
print "adjust ------------------------- done "
#for i in range(nb_wares):
#	if nb_allocated_drones[i] == 0
#		nb_allocated_drones[i] = 1
#

print allocated_drones
nb_allocated_drones = int(np.sum(allocated_drones))

print nb_allocated_drones

if filename == "busy_day.in":
	allocated_drones[0] -=1
	allocated_drones[1] +=1

index = 0
for i in range(nb_wares):
	for d in range(int(allocated_drones[i])):
		wares[i].assigned_drones.append(index)
		index += 1
	#print wares[i].assigned_drones

for w in wares:
	w.start()





















file_out.close()