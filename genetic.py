from __future__ import annotations
import random
import typing
import fastrand
import pygad
from data_preprocessing import DataSource
import numpy as np
# This array stores the number of the teacher that advise the thesis i
a = 6
b = 15

# similarity[i][j] = k means that the similarity score between teacher i and thesis j is k
# Read similarity score from similarity.txt


class Assignment:
    # self.thesis[i] = j means that the teacher number j will be assigned to defense the thesis number i

    def __init__(self, chromosome: typing.List, generation: int, data: DataSource):
        self.data = data
        self.advisor = []
        self.similarity = []
        self.num_of_thesis = data.num_of_thesis
        self.num_of_teacher = data.num_of_teacher
        if len(chromosome) != data.num_of_thesis:
            raise Exception(
                "Chromosome length is not equal to number of theses")

        self.thesis = []
        for i in range(len(chromosome)):
            self.thesis.append(chromosome[i])
        self.generation = generation
        self.advisor = data.advisor
        self.similarity = data.similarity
        self.fitness = self.fitness()
        self.min_count = data.min_count
        self.max_count = data.max_count
        self.minimum_similarity = data.minimum_similarity

    def __str__(self):
        return str(self.thesis) + " " + str(self.fitness)

    def __repr__(self):
        return str(self.thesis) + " " + str(self.fitness)

    # This function checks if the assignment is valid, i.e. no teacher is assigned to more than one thesis
    # If the assignment is valid, return 0, otherwise return the negative score, based on number of violations
    def check_valid(self):
        score = 0
        thesis_count = [0 for i in range(self.num_of_teacher)]
        a = self.data.min_count
        b = self.data.max_count
        minimum_similarity = self.data.minimum_similarity
        # Teacher should not be defense the thesis that they advise
        for i in range(self.num_of_thesis):
            if self.thesis[i] == self.advisor[i]:
                score -= 1
        # The number of thesis that each teacher is assigned to should be in the range [a, b]
        for i in range(self.num_of_thesis):
            thesis_count[self.thesis[i]] += 1
        for i in range(self.num_of_teacher):
            if a <= thesis_count[i] <= b:
                continue
            elif thesis_count[i] < a:
                score -= (a - thesis_count[i]) * 10
            else:
                score -= (thesis_count[i] - b) * 10
        if max(thesis_count) - min(thesis_count) > 12:
            score -= 1000

        # The similarity score between teacher and thesis should be greater than minimum_similarity
        for i in range(self.num_of_teacher):
            for j in range(self.num_of_thesis):
                if self.thesis[j] == i:
                    if self.similarity[j][i] < minimum_similarity:
                        score -= 1

        return score

    def fitness(self):
        valid_score = self.check_valid()
        if valid_score < 0:
            return valid_score
        score = 0

        for j in range(self.num_of_teacher):
            for i in range(self.num_of_thesis):
                if self.thesis[j] == i:
                    score += self.similarity[i][j]
        return score * 10


# if __name__ == "__main__":
#     ga_instance = get_ga_instance()
#     ga_instance.run()
#     # Get list of the best solutions
#     solution, solution_fitness, solution_idx = ga_instance.best_solution()
#     print(solution)
#     print(solution_fitness)
#     print(solution_idx)
