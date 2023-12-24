import typing
import os
from schema import Teacher, Thesis, AssignmentResponse
import numpy as np


class DataSource:
    def __init__(self):
        self.teachers = []
        self.theses = []
        self.similarity = []
        self.advisor = []
        self.load_teacher_from_file("data/teachers.txt")
        self.load_thesis_from_file("data/thesis_vi.csv")
        self.load_simiarity_from_file("data/similarity.csv")
        self.load_advisor_from_file("data/advisor.txt")
        self.num_of_teacher = len(self.teachers)
        self.num_of_thesis = len(self.theses)
        self.assignment: list[AssignmentResponse] = []

    def __str__(self):
        return f"Data source with {len(self.teachers)} teachers and {len(self.theses)} theses"

    def __repr__(self):
        return self.__str__()

    def get_teacher(self, id: int) -> Teacher:
        return self.teachers[id]

    def get_thesis(self, id: int) -> Thesis:
        return self.theses[id]

    def load_teacher_from_file(self, path: str = "teachers.txt"):
        # Read data from file
        teachers_specialties = {}
        with open(os.path.join(os.path.dirname(__file__), path), "r") as f:
            lines = f.readlines()
            teachers = []
            teacher = ""
            specialties = []
            for line in lines:
                if line.startswith("["):
                    # remove '
                    specialties = [line[1:-1]
                                   for line in line[1:-2].split(", ")]
                    teachers_specialties[teacher] = specialties

                else:
                    teacher = line[:-1]
        teacher_id = 0
        for teacher in teachers_specialties:
            self.teachers.append(Teacher(teacher_id, teacher,
                                         teachers_specialties[teacher], None))
            teacher_id += 1

    def load_thesis_from_file(self, path: str = "thesis_raw.csv"):
        # Read data from file
        theses = []
        thesis_id = 0
        with open(os.path.join(os.path.dirname(__file__), path), "r") as f:
            lines = f.readlines()
            theses = []
            # skip the first line
            lines = lines[1:]
            for line in lines:
                thesis = line.split(",", 1)
                # Remove double quotes
                thesis[1] = thesis[1].replace('"', "").replace(
                    "\n", "").replace('.\n', '')
                self.theses.append(
                    Thesis(thesis_id, thesis[1], None, thesis[0]))
                thesis_id += 1

    def load_simiarity_from_file(self, path: str = "similarity.csv"):
        similarity = []
        with open(os.path.join(os.path.dirname(__file__), path), "r") as f:
            lines = f.readlines()
            lines = lines[1:]
            for line in lines:
                line = line.replace("\n", "").split(",")
                # convert to float
                line = [float(score) for score in line[1:]]
                print(line)
                similarity.append(line)
        self.similarity = similarity

    def load_advisor_from_file(self, path: str = "data/advisor.txt"):
        advisor = []
        with open(os.path.join(os.path.dirname(__file__), path), "r") as f:
            line = f.readline()
            for i in range(len(self.theses)):
                advisor.append(int(line.split()[i]))
        self.advisor = advisor
    # save to datasource

    def save_assignment(self, assign: AssignmentResponse):
        # check if the assignment is duplicated
        # check array-wise
        for a in self.assignment:
            if a.fitness == assign.fitness:
                return
        self.assignment.append(assign)


# similarities = {}
# with open(os.path.join(os.path.dirname(__file__), "table_score.csv"), "r") as f:
#     lines = f.readlines()
#     lines = lines[1:]
#     for line in lines:
#         line = line.split(",")
#         similarities[line[0]] = line[1:]

# # Power transformation, apply to all similarities
# for student in similarities:
#     for i in range(len(similarities[student])):
#         if float(similarities[student][i]) <= 0:
#             print(float(similarities[student][i]))
#             print("Negative similarity")
#         similarities[student][i] = float(similarities[student][i]) ** 0.3

# # Normalize, keep in range [0, 1]
# for student in similarities:
#     print(similarities[student])
#     max_score = max(similarities[student])
#     for i in range(len(similarities[student])):
#         similarities[student][i] /= max_score
# # Write to file
# with open(os.path.join(os.path.dirname(__file__), "similarity.txt"), "w") as f:
#     for teacher in similarities:
#         for i in range(len(similarities[teacher])):
#             f.write(str(similarities[teacher][i]) + " ")
#         f.write("\n")
