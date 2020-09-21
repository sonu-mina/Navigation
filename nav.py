from random import uniform, randint
import matplotlib.pyplot as plt
import numpy as np
from heapq import heapify, heappush, heappop
import time
from queue import PriorityQueueYY

class Map:
    
	
	# Define Variables
	points = []
	start = []


	# Define Starting Point
	def defineStart(self):
		print("Enter Starting Point : ")
		x, y = input("Enter x : "), input("Enter y : ")
		# x, y = 1, 2
		self.start = Point(float(x), float(y))
		return self.start

	def defineDestination(self):
		print("Enter destination Point : ")
		x, y = input("Enter x : "), input("Enter y : ")
		self.dest = Point(float(x), float(y))
		return self.dest


	def bakePath(self, n, l, w):
		'''
			Build the points and the paths between them
			Args:
				n = no of points
				l = length
				w = width
		'''

		# Build Points
		for x in range(n):
			self.points.append(Point(uniform(0, l), uniform(0, w)))

		# Build Connections for each point
		for i in range(n):
			n_connections = randint(0, int(n))
			if i%100==0:
				print("processing " + str(i+1) + "th point")

			for j in range(n_connections):
				toAppend = randint(0, n-1)
				if (self.points[i].isValid(self.points[toAppend], 0.7)):
					self.points[i].connections.add(toAppend)
					# choose = uniform(0, 1)
					# if choose>0.5 or True:
					self.points[toAppend].connections.add(i) # Comment later

		# for i in range(n):
		# 	self.points[i].connections = list(self.points[i].connections)


	# Show the whole roadmap with all the connections
	def showAllConnections(self):
		pts_x = [pt.x for pt in self.points]
		pts_y = [pt.y for pt in self.points]
		plt.scatter(pts_x, pts_y)
		n = len(self.points)
		for i in range(n):
			for j in range(len(self.points[i].connections)):
				xs = [self.points[i].x, self.points[self.points[i].connections[j]].x]
				ys = [self.points[i].y, self.points[self.points[i].connections[j]].y]
				plt.plot(xs, ys, c='g')
		plt.show()


	# Show Start with nearest neighbours
	def showStart(self):
		dist = float('inf')
		for x in self.points:
			if(self.start.distance(x)<dist):
				nearest = x
				dist = self.start.distance(x)
		plt.scatter(self.start.x, self.start.y, c='r', zorder=2)
		pts_x = [pt.x for pt in self.points]
		pts_y = [pt.y for pt in self.points]
		plt.scatter(pts_x, pts_y)
		n = len(self.points)
		for i in range(n):
			for j in range(len(self.points[i].connections)):
				xs = [self.points[i].x, self.points[self.points[i].connections[j]].x]
				ys = [self.points[i].y, self.points[self.points[i].connections[j]].y]
				plt.plot(xs, ys, c='g', zorder=1)
		plt.plot([self.start.x, nearest.x], [self.start.y, nearest.y], c='r', zorder=2)
		dest = self.points[0]
		plt.scatter(dest.x, dest.y, c='y', zorder=2)
		plt.show()


	def showPath(self, path):
		'''
			Show Start with nearest neighbours
		'''

		for i in range(len(self.points)):
			self.points[i].connections = list(self.points[i].connections)

		# plt.figure(figsize=(20, 20), facecolor='w', edgecolor='k')
		dist = float('inf')
		for x in self.points:
			if(self.start.distance(x)<dist):
				nearest = x
				dist = self.start.distance(x)
		
		n = len(self.points)
		for i in range(n):
			for j in range(len(self.points[i].connections)):
				xs = [self.points[i].x, self.points[self.points[i].connections[j]].x]
				ys = [self.points[i].y, self.points[self.points[i].connections[j]].y]
				plt.plot(xs, ys, c='lightgray', zorder=1)
		
		plt.plot([self.start.x, nearest.x], [self.start.y, nearest.y], c='y', zorder=2)
		dest = self.points[0]

		pts_x = [pt.x for pt in self.points]
		pts_y = [pt.y for pt in self.points]
		plt.scatter(pts_x, pts_y, c='grey', zorder=1.2, s=10)
		
		# Show Path
		xs = [self.points[pt].x for pt in path]
		ys = [self.points[pt].y for pt in path]
		plt.plot(xs, ys, c='b', zorder=2)
		plt.scatter(self.start.x, self.start.y, c='#000000', zorder=2)
		plt.scatter(self.dest.x, self.dest.y, c='#a1122a', zorder=2)

		plt.axis('off')
		plt.show()


	# Find starting point in saved points
	def findStart(self, start):
		dist = float('inf')
		for i, x in enumerate(self.points):
			if(self.start.distance(x)<dist):
				nearest = i
				dist = self.start.distance(x)
		return nearest

	def findDestination(self, dest):
		dist = float('inf')
		for i, x in enumerate(self.points):
			if(self.dest.distance(x)<dist):
				nearest = i
				dist = self.dest.distance(x)
		print(str(self.points[nearest]))
		return nearest


	def getPath(self, start, dest):
		'''
			Get Path from current position
		'''

		start_time = time.time()
		path = []
		points = self.points
		starting, destination = self.points[start], self.points[dest]
		print("start:"+str(start))
		print("starting : " + str(starting))

		# each element of all paths is stored as below
		# d = distance_covered_till_now
		# d1 = distance from destination
		# [
		# 	d+d1, 
		# 	d, 
		# 	index_of_current_position, 
		# 	coming_from_index
		# ]
		all_paths = [[starting.distance(destination), 0, start, -1]]
		dist = float('inf')
		coming_from_relations = {}

		# visited = [False for i in range(len(points))]
		# orders = [0 for i in range(len(points))]
		# curr_order = 1

		while len(all_paths):
			curr = all_paths[0]
			heappop(all_paths)
			curr_index, dist_covered_till_now = curr[2], curr[1]
			print("curr_index:"+str(curr_index)+"  printing connections for " + str(points[curr_index])+' : '  + str([str(points[con]) for con in points[curr_index].connections]))
			
			for i, conn in enumerate(points[curr_index].connections):
				print("conn : " + str(self.points[conn]))
				if conn==dest:

					coming_from_relations[conn] = curr_index
					print(coming_from_relations)
					path.append(conn)
					while(conn in coming_from_relations) and conn!=start:
						print("conn : " + str(conn) + '--' + str(points[conn]))
						path.append(coming_from_relations[conn])
						conn = coming_from_relations[conn]
					for i in path:
						print(self.points[i])
					print("Time taken : " + str(time.time()-start_time))
					return path

				d = points[curr_index].distance(points[conn])+dist_covered_till_now
				d1 = destination.distance(points[conn])

				# If it's a loop , do nothing
				# if (curr_index in coming_from_relations):# and (coming_from_relations[curr_index]==conn):
				# 	temp_curr_index = curr_index
				# 	changed = False
				# 	while(temp_curr_index in coming_from_relations):
				# 		temp_curr_index = coming_from_relations[temp_curr_index]
				# 		if temp_curr_index==conn:
				# 			changed = True
				# 			break
				# 	if changed:
				# 		continue
				# coming_from_relations[conn] = curr_index
				# print("indexed")

				try:
					if conn in coming_from_relations:
						index = list(np.array(all_paths)[:, 2]).index(conn)
						if(d<all_paths[index][1]):
							# print("found a shorter way!\n")
							all_paths[index][1] = d
							all_paths[index][0] = d+d1
							all_paths[index][3] = curr_index
							heapify(all_paths)
							coming_from_relations[conn] = curr_index
					else:
						raise ValueError() # This will give valueerror and will go into except

				except (IndexError, ValueError):
					if conn in coming_from_relations:
						# print("It has already been popped out, SORRY !! Moving ahead!!")
						continue
					# print("push")
					heappush(all_paths, [d+d1, d, conn, curr_index])
					coming_from_relations[conn] = curr_index			



	# Get path function refreshed
	def getPathNew(self, start, dest):
		start_time = time.time()
		path = []
		pts = self.points
		n_pts = len(pts)
		starting, destination = self.points[start], self.points[dest]
		dist, prev = [float('inf')]*n_pts, [-1]*n_pts
		dist[start] = 0
		pq = PriorityQueue()
		pq.put([pts[start].distance(pts[dest]), start])

		while(not pq.empty()):
			elem = pq.get()[1]
			if(elem==dest):
				while (elem>=0 and elem<n_pts):
					path.append(elem)
					elem = prev[elem]
				print(path)
				print("Time taken :" + str(time.time()-start_time))
				return path

			print(pts[elem])
			for conn in pts[elem].connections:
				d = pts[elem].distance(pts[conn])
				if(dist[conn]>dist[elem]+d):
					dist[conn] = dist[elem]+d
					prev[conn] = elem
					pq.put([dist[conn]+pts[conn].distance(pts[dest]), conn])