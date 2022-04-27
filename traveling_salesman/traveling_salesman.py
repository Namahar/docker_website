import random
import dijkstra
import lexicographic_order
import genetic_algorithm

def get_points(num_points):
   locations = list()

   for i in range(num_points):
      l = [random.random() * 10 * num_points, random.random() * 10 * num_points]
      locations.append(l)

   return locations

def dijkstra_method(num_points, locations):
   graph = dijkstra.Graph(locations)

   print('Dijkstra Algorithm')
   print('time taken = ' + str(graph.end) + ' seconds')
   print(graph.order, graph.distance)
   print()

   return

def genetics(num_points, locations):
   genes = genetic_algorithm.Genes(num_points, locations)

   print('Genetic Algorithm')
   print('time taken = ' + str(genes.end) + ' seconds')
   print(genes.min_order, genes.min_distance)
   print()

   return

def brute_force(num_points, locations):
   lexicographic = lexicographic_order.Lexicographic(num_points, locations)

   # distance, order, time = lexicographic_order.animate_search(num_points, locations)
   print('Lexicographic algoirthm')
   print('time taken = ' + str(lexicographic.end) + ' seconds')
   print(lexicographic.min_order, lexicographic.min_distance)
   print()
   

   return

def main():

   # get location data
   num_points = 5
   locations = get_points(num_points)
   # print(locations)

   # dijkstra method implementation
   dijkstra_method(num_points, locations)

   # genetic algorithm
   genetics(num_points, locations)

   # brute force method implementation
   brute_force(num_points, locations)

   print()

   return

if __name__ == '__main__':
   main()