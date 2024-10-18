import math
import random
import time #limit execution time to 1 minute

# ELITIST ANT COLONY OPTIMISATION ALGORITHM TO SOLVE THE TSP PROBLEM

print(f"Num cities: {num_cities}")
# clip dist_matrix to 100
if num_cities > 100:
    num_cities = 100
    dist_matrix = dist_matrix[:100][:100]

num_ants = num_cities
max_it = 100
bestTour = []
bestDistance = math.inf
bestNNDistance = math.inf
bestNNTour = []
nn_tour_cache = {}

def tour_length(tour):
    length = 0
    for i in range(num_cities - 1):
        # print(f"City: {tour[i]}, next city: {i+1}, dist: , length: {length}, len(tour): {len(tour)}")
        length = length + dist_matrix[tour[i]][tour[i + 1]]
    length = length + dist_matrix[tour[num_cities - 1]][tour[0]]
    return length


def nearest_neighbour(city,visited):
    minDist = math.inf 
    nearest = -1
    for i in range(num_cities):
        if i not in visited and dist_matrix[city][i] < minDist:
            # print(f"City: {city}, i: {i}, dist: {dist_matrix[city][i]}, nearest: {nearest}")
            if dist_matrix[city][i] == 0:
                return i
            minDist = dist_matrix[city][i]
            nearest = i
    if nearest == -1:
        return None
    else:
        return nearest

def nearest_neighbour_tour(start):
    global nn_tour_cache
    if start in nn_tour_cache:
        return nn_tour_cache[start]
    
    global bestNNDistance
    global bestNNTour
    tour = []
    visited = []
    city = start
    visited.append(city)
    tour.append(city)

    if time.time() - start_time > 30:
        return bestNNTour
    
    for i in range(num_cities):
        # print(f"i: {i}, city: {city}, visited: {visited}")
        if len(visited) == num_cities:
            break
        city = nearest_neighbour(city,visited)
        if city == None:
            break
        visited.append(city)
        tour.append(city)

    if len(tour) < num_cities:
        for i in range(num_cities):
            if i not in visited:
                visited.append(i)
                tour.append(i)
                break

    length = tour_length(tour)
    if length < bestNNDistance and len(tour) == num_cities:
        bestNNDistance = length
        bestNNTour = tour

    nn_tour_cache[start] = tour 
    return tour

def visit_next(city,visited,pheromone):
    alpha = 1
    beta = 2
    probs = []
    total = 0
    for i in range(num_cities):
        if i not in visited: # 1. has the city been visited?
            if dist_matrix[city][i] == 0 and i != city:
                return i
            total = total + (pheromone[city][i]**alpha)*(1/dist_matrix[city][i])**beta #2. pheromone_level^alpha * heuristic_desirability^beta -

    for i in range(num_cities):
        if i in visited:
            probs.append(0)
        else:
            probs.append((pheromone[city][i]**alpha)*(1/dist_matrix[city][i])**beta/total)
    return random.choices(range(num_cities),probs)[0]

def calculate_nn_distances():
    nn_distances = [tour_length(nearest_neighbour_tour(i)) for i in range(num_cities)]
    return nn_distances 
        
def ant_colony_optimisation(num_ants,max_it):
    global bestDistance
    global bestTour
    rho = 0.5 #evaporation rate
    w = 50 #elistist ants
    start_time = time.time()

    # initialise pheromone deposit
    nn_distances = calculate_nn_distances() 
    pheromone = [[num_ants / nn_distances[i] for i in range(num_cities)] for j in range(num_cities)]
    # pheromone = [[num_ants/tour_length(nearest_neighbour_tour(i)) for i in range(num_cities)] for j in range(num_cities)] # inefficient option of initialising pheromone levels
    # pheromone = [[(w+num_ants)/(rho*tour_length(nearest_neighbour_tour(i))) for i in range(num_cities)] for j in range(num_cities)]
    for i in range(max_it):
        for j in range(num_ants): # for each ant
            tour = []
            visited = []
            city = random.randint(0,num_cities-1) # choose a random city to start
            visited.append(city)
            tour.append(city)
            for k in range(1,num_cities): 
                city = visit_next(city,visited,pheromone) 
                visited.append(city)
                tour.append(city)

            # update best tour    
            tour_dist = tour_length(tour)
            if tour_dist < bestDistance:
                bestDistance = tour_dist
                bestTour = tour
            
            # update pheromone levels
            for k in range(num_cities - 1):
                pheromone[tour[k]][tour[k+1]] = (1-rho)*pheromone[tour[k]][tour[k+1]] + 1/tour_dist
            pheromone[tour[num_cities-1]][tour[0]] = (1-rho)*pheromone[tour[num_cities-1]][tour[0]] + 1/tour_dist

            # additional reinforcement of best tour
            for k in range(num_cities - 1):
                pheromone[bestTour[k]][bestTour[k+1]] += w/bestDistance
            pheromone[bestTour[num_cities-1]][bestTour[0]] += w/bestDistance

        if time.time() - start_time > 58:
            # print("Time limit reached at iteration: ", i)
            break

    return bestTour,bestDistance

tour, tour_length = ant_colony_optimisation(num_ants,max_it)
