from typing import Union, List
import pygad
from pydantic import BaseModel

from fastapi import FastAPI, Query
from data_preprocessing import DataSource
from genetic import Assignment
from schema import Teacher, Thesis, AssignmentResponse, AssignmentNew, TeacherAssigment, ThesisInfo
app = FastAPI()
data = DataSource()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/teachers")
def read_teachers():
    return data.teachers


@app.get("/teachers/{teacher_id}")
def read_teacher(teacher_id: int):
    return data.teachers[teacher_id]


@app.get("/theses")
def read_theses():
    return data.theses


@app.get("/theses/{thesis_id}")
def read_thesis(thesis_id: int):
    return data.theses[thesis_id]


@app.get("/similarity")
def read_similarity():
    return data.similarity

# example
# http://localhost:8000/similarity/teacher/1/thesis/1


@app.get("/similarity/teacher/{teacher_id}/thesis/{thesis_id}")
def read_similarity(teacher_id: int, thesis_id: int):
    teacher_name = data.teachers[teacher_id].name
    thesis_name = data.theses[thesis_id].name
    student_name = data.theses[thesis_id].student
    return {"teacher": teacher_name, "thesis": thesis_name, "student": student_name, "similarity": data.similarity[teacher_id][thesis_id]}


@app.get("/advisor/thesis/{thesis_id}")
def read_advisor(thesis_id: int):
    teacher_id = data.advisor[thesis_id]
    teacher_name = data.teachers[teacher_id].name
    thesis_name = data.theses[thesis_id].name
    student_name = data.theses[thesis_id].student
    return {"teacher": teacher_name, "thesis": thesis_name, "student": student_name, "teacher_id": teacher_id}


@app.get("/advisor")
def read_advisors():
    return data.advisor


@app.get("/assignment")
def get_assignment() -> List[AssignmentResponse]:
    ga_instance = get_ga_instance()
    ga_instance.run()
    data.assignment.sort(key=lambda x: x.fitness, reverse=True)
    return data.assignment

# limit


@app.get("/assignment/v2")
def get_assignment_v2(limit: int = Query(default=10, ge=1, le=20)) -> List[AssignmentNew]:
    while data.assignment == []:
        ga_instance = get_ga_instance()
        ga_instance.run()
    data.assignment.sort(key=lambda x: x.fitness, reverse=True)
    result: list[AssignmentNew] = []
    for assignment in data.assignment[:limit]:
        teachers = []
        for i in range(data.num_of_teacher):
            teacher = TeacherAssigment(
                teacher=data.teachers[i].name, theses=[])
            for j in range(data.num_of_thesis):
                if assignment.assignment[j] == i:
                    thesis = ThesisInfo(
                        thesis=data.theses[j].name, student=data.theses[j].student, similarity=data.similarity[j][i])
                    teacher.theses.append(thesis)
            teachers.append(teacher)
        result.append(AssignmentNew(
            teachers=teachers, total_similarity=assignment.fitness))

    return result


def fitness_func(ga_instance, solution, solution_index):
    a = Assignment(solution, 0, data)
    return a.fitness


fitness_function = fitness_func
gene_type = int
num_generations = 1000
num_parents_mating = 4
sol_per_pop = 8
num_genes = data.num_of_thesis

init_range_low = 0
init_range_high = data.num_of_teacher

parent_selection_type = "sss"
keep_parents = 1

crossover_type = "two_points"

mutation_type = "random"
mutation_percent_genes = 2


def on_generation(ga_instance: pygad.GA):
    # append the fitness value of the best solution in the current population to the fitness_history list
    if ga_instance.best_solutions_fitness[-1] > 0:
        best_solution, best_solution_fitness, _ = ga_instance.best_solution()
        a = AssignmentResponse(assignment=best_solution,
                               fitness=best_solution_fitness)
        data.save_assignment(a)


def get_ga_instance() -> pygad.GA:
    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           init_range_low=init_range_low,
                           init_range_high=init_range_high,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_percent_genes=mutation_percent_genes,
                           gene_type=gene_type,
                           on_generation=on_generation
                           )
    return ga_instance
