import random
import math
import time
import scipy.spatial.distance as ssd
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

class Genes:
   def __init__(self, num_points, locations):
      self.start = time.time()
      self.num_points = num_points
      self.locations = locations

      self.pop_size = num_points * 3
      self.mutation_rate = 0.01
      self.min_distance = [math.inf]
      self.min_order = list()
      self.fitness = list()
      self.num_generations = 1
      self.max_generations = self.num_points * 10

      self.population = self.create_population()

      # run simulation
      # while self.num_generations < self.max_generations:
      #    self.life()
      #    self.num_generations += 1

      self.show_plot()

      self.end = time.time() - self.start

      return

   def create_population(self):
      adam = [i for i in range(self.num_points)]
      population = list()

      for i in range(self.pop_size):
         population.append(adam)
         random.shuffle(adam)

      return population

   def life(self):
      self.calc_fitness()

      self.normalize_fitness()

      self.evolve()
      
      return

   def calc_fitness(self):
      self.fitness.clear()

      for p in self.population:
         length = len(p) - 1

         total = 0
         for i in range(length):
            total += ssd.euclidean(self.locations[p[i]], self.locations[p[i+1]])

         if total < self.min_distance[0]:
            self.min_distance[0] = total
            self.min_order.clear()
            self.min_order.extend(p)

         self.fitness.append(1 / (math.pow(total, 8) + 1) )

      return

   def normalize_fitness(self):
      summation = 0
      for val in self.fitness:
         summation += val

      for i in range(len(self.fitness)):
         self.fitness[i] /= summation

      return

   def choose(self):
      index = 0
      rate = random.random()

      while rate > 0:
         rate -= self.fitness[index]
         index += 1

      index -= 1

      if index > len(self.population):
         index = len(self.population) - 1

      return self.population[index].copy()

   def crossover(self, order_1, order_2):
      length = len(order_1) - 1
      start = math.floor(random.randint(0, length))
      end = math.floor(random.randint(start + 1, length+1))

      order = order_1[start : end]

      for val in order_2:
         if val not in order:
            order.append(val)

      return order

   def evolve(self):
      new_gen = list()

      for i in range(len(self.population)):
         order_1 = self.choose()
         order_2 = self.choose()

         order = self.crossover(order_1, order_2)
         self.mutate(order)
         new_gen.append(order)

      self.population.clear()
      self.population.extend(new_gen)

      return

   def mutate(self, order):
      length = len(order)

      for l in range(length):
         if random.random() < self.mutation_rate:
            i = math.floor(random.randint(0, length-1))
            j = (i + 1) % length
            
            temp = order[i]
            order[i] = order[j]
            order[j] = temp

      return

   def update(self, frame):
      self.life()
      self.num_generations += 1

      # plot locations
      # clear previous graphs
      self.ax.clear()

      # make titles the order being shown
      self.ax.title.set_text('Generation ' + str(self.num_generations) + ' Best Order = ' + str(self.min_order))

      # add index labels to points
      x = list()
      y = list()
      for i in self.min_order:
         self.ax.annotate(str(i), (self.locations[i][0], self.locations[i][1]))
         x.append(self.locations[i][0])
         y.append(self.locations[i][1])

         self.ax.plot(x, y, marker='.', markersize=12.0)

      return

   def show_plot(self):

      self.fig = plt.figure('Genetic Order')
      self.ax = self.fig.add_subplot(1, 1, 1)

      # start plot
      # args = (ax)
      animate = animation.FuncAnimation(self.fig, self.update, frames=self.max_generations)

      animate.save('genetic.mp4')

      return
