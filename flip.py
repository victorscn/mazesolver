class Flip():
	
	def __init__(self, dist, maze_dim):
		self.distance = list(dist)
		self.maze_dim = maze_dim
		self.dist_goal = self.distance[0][0]

	def go(self):
		result = [[0 for col in range(self.maze_dim)] for row in range(self.maze_dim)]
		#The goal is the first cell, so: x,y = 0,0
		for y in range(self.maze_dim):
			for x in range(self.maze_dim):
				flip_value = self.dist_goal - self.distance[y][x]				
				if flip_value > 0:
					result[y][x] = flip_value
				elif x==0 and y == 0:					
					result[y][x] = 0
				else:								
					result[y][x] = 255
		return result

	def ungo(self, fl):
		flipped = list(fl)
		for y in range(self.maze_dim):
			for x in range(self.maze_dim):
				if flipped[y][x] <= 255 :
					if flipped[y][x] > flipped[0][0]:
						self.distance[y][x] == 255
					else:
						self.distance[y][x] = flipped[y][x]
		return self.distance