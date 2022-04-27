import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import math
import scipy.spatial.distance as ssd
import time

class Lexicographic:
   def __init__(self, num_points, locations):
      self.start = time.time()
      self.num_points = num_points
      self.locations = locations
      self.min_distance = math.inf
      self.min_order = list()
      self.lexicographic_order = [i for i in range(num_points)]
      self.finish = False

      self.animate_search()

      self.end = time.time() - self.start

      return


   def distance(self):

      # calculate distance
      total_distance = 0
      for i, index in enumerate(self.lexicographic_order):

         # prevent oob indexing
         if i == len(self.lexicographic_order) - 1:
            break
         
         # get location of a point in the order and location of following point
         current_loc = self.locations[index]
         next_loc = self.locations[self.lexicographic_order[i+1]]
         total_distance += ssd.euclidean(current_loc, next_loc)

      # store shortest distance and location sequence
      if total_distance < self.min_distance:
         self.min_distance = total_distance
         self.min_order.clear()
         self.min_order.extend(self.lexicographic_order)

      return

   
   def swap(self, i, j):
      temp = self.lexicographic_order[i]
      self.lexicographic_order[i] = self.lexicographic_order[j]
      self.lexicographic_order[j] = temp
      return

   def lexo_order(self):

      # find second largest number in array with given order
      largest_i = -1
      for i in range(len(self.lexicographic_order) - 1):
         if self.lexicographic_order[i] < self.lexicographic_order[i+1]:
            largest_i = i

      # if no number found, all permutations have been done
      if largest_i == -1:
         self.finish = True
         return
      
      # find index with number larger than number at index i
      largest_j = -1
      for j in range(len(self.lexicographic_order)):
         if self.lexicographic_order[largest_i] < self.lexicographic_order[j]:
            largest_j = j

      # swap two values
      self.swap(largest_i, largest_j)

      # reverse array from largest_i + 1 to end
      sliced = self.lexicographic_order[largest_i+1:]

      # store order beginning of order
      keep = self.lexicographic_order[0: largest_i + 1]

      # reverse sliced and add back to keep list
      sliced.reverse()
      keep.extend(sliced)
      
      # clear lexicographic list for new order
      self.lexicographic_order.clear()
      self.lexicographic_order.extend(keep)

      return

   def split(self, order):
      x = list()
      y = list()

      for o in order:
         point = self.locations[o]
         x.append(point[0])
         y.append(point[1])

      return x, y

   def update(self, frame):

      # split locations into x and y coordinates for graphing
      x, y = self.split(self.lexicographic_order)

      # calculate distance
      self.distance()

      best_x, best_y = self.split(self.min_order)

      # plot locations
      # clear previous graphs
      self.ax1.clear()
      self.ax2.clear()

      # make titles the order being shown
      self.ax1.title.set_text('Best Order = ' + str(self.min_order))
      self.ax2.title.set_text(str(self.lexicographic_order))

      # add index labels to points
      for i in range(self.num_points):
         self.ax1.annotate(str(i), (self.locations[i][0], self.locations[i][1]))
         self.ax2.annotate(str(i), (self.locations[i][0], self.locations[i][1]))

      self.ax1.plot(best_x, best_y, marker='.', markersize=12.0, color='red')
      self.ax2.plot(x, y, marker='.', markersize=12.0)

      # update order
      self.lexo_order()

      return

   def animate_search(self):
      # plot variables
      self.fig = plt.figure('Lexicographic Order: Brute Force')
      self.fig.subplots_adjust(hspace=0.5)
      self.ax1 = self.fig.add_subplot(2, 1, 1)
      self.ax2 = self.fig.add_subplot(2, 1, 2)

      # start plot
      num_frames = math.factorial(self.num_points)
      animate = animation.FuncAnimation(self.fig, self.update, frames=num_frames)

      animate.save('lexicographic.mp4')

      return