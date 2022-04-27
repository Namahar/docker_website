import math
import matplotlib.pyplot as plt
from time import time

class Vertex:
   def __init__(self, location):
      self.x = location[0]
      self.y = location[1]
      self.neighbors = list()
      self.distances = list()

      return

   def add_neighbors(self, key, length):
      for i in range(length):
            if i != key:
               self.neighbors.append(i)

      return

   def add_distance(self, vertices, neighbor):
      vertex = vertices[neighbor]
      x = (self.x - vertex.x)**2
      y = (self.y - vertex.y)**2
      d = (x + y)**0.5
      self.distances.append(d)

      return

class Graph:
   def __init__(self, locations):
      self.start = time()
      self.vertices = dict()
      self.num_vertices = 0
      self.locations = locations

      # create graph
      self.fill_graph()
      self.add_edges()
      self.calc_distance()

      # calculate route distances
      self.routes = self.dijkstra()
      self.order, self.distance = self.find_path()

      self.end = time() - self.start

      # save graph
      self.plot_graph()

      return

   def add_vertex(self, vertex):
      self.vertices[self.num_vertices] = vertex
      self.num_vertices += 1

      return

   def add_edges(self):
      for key, vertex in self.vertices.items():
         vertex.add_neighbors(key, self.num_vertices)

      return

   def calc_distance(self):
      for key, vertex in self.vertices.items():
         for neighbor in vertex.neighbors:
            vertex.add_distance(self.vertices, neighbor)

      return

   def fill_graph(self):
      for loc in self.locations:
         point = Vertex([loc[0], loc[1]])
         self.add_vertex(point)

      return

   def print_graph(self):
      for key, val in self.vertices.items():
         print('key = ' + str(key))
         print('location = ' + str(val.x) + '\t' + str(val.y))
         print('neighbors = ' + str(val.neighbors))
         print('distances = ' + str(val.distances))
         print()

      return

   def dijkstra(self):
      scores = dict()

      # use each node as a starting point
      for i in range(self.num_vertices):

         # get vertex object
         start_vertex = self.vertices[i]
         
         unvisited = [k for k in range(self.num_vertices)]
         visited = list()
         distance = 0

         visited.append(unvisited.pop(i))
         
         while len(unvisited) > 0:
            # check neighbors of vertex for shortest distance
            lowest_distance = math.inf
            next_neighbor = math.inf
            for j in range(len(start_vertex.neighbors)):
               if start_vertex.distances[j] < lowest_distance:
                  if start_vertex.neighbors[j] in unvisited:
                     lowest_distance = start_vertex.distances[j]
                     next_neighbor = start_vertex.neighbors[j]

            distance += lowest_distance

            # go to next node
            index = unvisited.index(next_neighbor)
            v = unvisited.pop(index)
            visited.append(v)
            start_vertex = self.vertices[next_neighbor]

         visited.append(distance)
         scores[i] = visited

      return scores

   def find_path(self):
      min_val = math.inf
      min_order = list()
      for key, val in self.routes.items():
         # print(val)
         if val[self.num_vertices] < min_val:
            min_val = val[self.num_vertices]
            min_order = val[0:self.num_vertices]

      return min_order, min_val

   def plot_graph(self):
      fig = plt.figure('Dijkstra Algorithm')
      ax = fig.add_subplot(1, 1, 1)

      # set title of graph to order being shown
      ax.title.set_text('Best Order = ' + str(self.order))

      # add index labels to points
      x = list()
      y = list()
      for i in self.order:
      # for i in range(self.num_vertices):
         ax.annotate(str(i), (self.locations[i][0], self.locations[i][1]))
         x.append(self.locations[i][0])
         y.append(self.locations[i][1])

      ax.plot(x, y, marker='.', markersize=12.0)

      plt.savefig('dijkstra_algorithm_graph.png')
