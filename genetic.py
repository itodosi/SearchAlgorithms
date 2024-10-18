import random
import math
import time #limit execution time to one minute

pop_size = num_cities
max_it = 5000
population = []
fitness = []
bestDistance = math.inf;
bestTour = [];

def tour_length(tour):
    length = 0
    for i in range(num_cities - 1):
        length = length + dist_matrix[tour[i]][tour[i + 1]]
    length = length + dist_matrix[tour[num_cities - 1]][tour[0]]
    return length

cities = []
for i in range(num_cities):
    cities.append(i)

def generate_random_tour():
    random_tour = cities.copy()
    random.shuffle(random_tour)
    return random_tour

def generate_population(pop_size):
    for i in range(pop_size):
        generated_tour = generate_random_tour()
        population.append(generated_tour)
        fitness.append(calculate_fitness(generated_tour))


def calculate_fitness(individual):
    global bestDistance
    global bestTour
    length = tour_length(individual)
    fitness = 1/(length+1) # higher tour length => lower fitness value => worse tour (added +1 just in case tour length is 0, which is improbable)
    updateBestTour(length, individual)
    return fitness #TODO: normalise fitness?

def create_child(tour1, tour2):
    new_tour = []
    for i in range(num_cities//2):
        new_tour.append(tour1[i])
    for i in range(num_cities//2, num_cities):
        new_tour.append(tour2[i])

    # check for duplicates and replace with not visited cities
    visited = []
    for i in range(num_cities):
        if new_tour[i] in visited:
            for j in range(num_cities):
                if tour2[j] not in visited:
                    new_tour[i] = tour2[j]
                    visited.append(tour2[j])
                    break
        else:
            visited.append(new_tour[i])
    
    return new_tour

def updateBestTour(length, tour):
    global bestDistance
    global bestTour
    if length < bestDistance:
        bestDistance = length
        bestTour = tour

def crossover(tour1, tour2):
    global bestDistance
    global bestTour

    #combine the two tours to create two children
    child1 = create_child(tour1, tour2)
    child2 = create_child(tour2, tour1)

    length1 = tour_length(child1)
    length2 = tour_length(child2)

    # choose the favourite child (the one with the shortest tour length)
    if length1 < length2:
        new_tour = child1
        length = length1
    else:
        new_tour = child2
        length = length2

    updateBestTour(length, new_tour)  
    return new_tour


def mutate(tour):
    # randomly choose 2 cities in the tour
    city1 = random.randint(0, num_cities - 1)
    city2 = random.randint(0, num_cities - 1)

    # swap the cities
    tour[city1], tour[city2] = tour[city2], tour[city1]
    return tour

def genetic_algorithm(pop_size, max_it):
    start_time = time.time()

    global population
    generate_population(pop_size)
    for i in range(max_it): #repeat until max_it (OPTIONAL: until some individual is fit enough)
        new_population = []
        for j in range(pop_size):
            individual1 = random.choices(population, weights=fitness,k=1)[0]
            individual2 = random.choices(population, weights=fitness,k=1)[0]
            new_tour = crossover(individual1, individual2)
            if random.random() < 0.1:
                new_tour = mutate(new_tour)
                updateBestTour(tour_length(new_tour), new_tour)
            new_population.append(new_tour)
        population = new_population.copy()
        if time.time() - start_time > 58:
            print("Time limit reached")
            break
        

genetic_algorithm(pop_size,max_it)

tour = bestTour
tour_length = tour_length(tour)
