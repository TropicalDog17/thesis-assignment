import random

# This array stores the number of the teacher that advise the thesis i
advisor = []
a = 1
b = 10
similarity = [[]]


class Assignment:
    # self.thesis[i] = j means that the teacher number j will be assigned to defense the thesis number i
    thesis = []

    def __init__(self, chromosome, generation):
        for i in range(chromosome):
            self.thesis[i] = chromosome[i]
        self.generation = generation
        self.fitness = 0

    def __str__(self):
        return str(self.thesis) + " " + str(self.fitness)

    def __repr__(self):
        return str(self.thesis) + " " + str(self.fitness)

    # This function checks if the assignment is valid, i.e. no teacher is assigned to more than one thesis
    # If the assignment is valid, return 0, otherwise return the negative score, based on number of violations
    def check_valid(self):
        score = 0

        # Teacher should not be defense the thesis that they advise
        for i in range(len(self.thesis)):
            if self.thesis[i] == advisor[i]:
                score -= 1

        # The number of thesis that each teacher is assigned to should be in the range [a, b]
        # a = 1, b = 10
        for i in range(len(advisor)):
            count = 0
            for j in range(len(self.thesis)):
                if self.thesis[j] == i:
                    count += 1
            if count < a or count > b:
                score -= 1
        # Similarity score between teacher and their assigned thesises should be in the range [0.5, 1]
        # similarity[i][j] = k means that the similarity score between teacher i and thesis j is k
        for i in range(len(advisor)):
            for j in range(len(self.thesis)):
                if self.thesis[j] == i:
                    if similarity[i][j] < 0.5 or similarity[i][j] > 1:
                        score -= 1

        return score

    def __lt__(self, other):
        if self.fitness == other.fitness:
            return self.generation < other.generation
        return self.fitness < other.fitness

    # This function is used to mate two assignments
    # Based on the cpp code above

    def mate(self, other):
        child_chromosome = []
        for i in range(len(self.thesis)):
            if random.randint(0, 1):
                child_chromosome.append(self.thesis[i])
            else:
                child_chromosome.append(other.thesis[i])
        # Randomly mutate some genes
        for i in range(len(self.thesis)):
            if random.random() < 0.5:
                child_chromosome[i] = random.randint(0, len(advisor) - 1)
        return Assignment(child_chromosome, self.generation)

    def gen_random_chromosome(self):
        chromosome = []
        for i in range(len(advisor)):
            chromosome.append(random.randint(0, len(advisor) - 1))
        return chromosome
# Given the initial population, this function returns the best assignment


def get_optimal_assignment(initial_pop):
    # Sort the initial population
    initial_pop.sort()
    # Return the best assignment
    return initial_pop[0]
