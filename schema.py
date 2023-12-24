from typing import Optional, List, AnyStr
from pydantic import BaseModel


class Teacher:
    """Teacher is a class that represents a teacher

    Args:
        id (int): Teacher id
        name (str): Teacher name
        specialty (List[str]): List of specialties
        thesis (Optional[int]): Thesis id
    """

    def __init__(self, id: int, name: str, specialty: List[AnyStr], thesis: Optional[int]):
        self.id = id
        self.name = name
        self.thesis = thesis
        self.specialty = specialty

    def __str__(self):
        return f"Teacher {self.id}: {self.name}"

    def __repr__(self):
        return self.__str__()


class Thesis:
    """Thesis is a class that represents a thesis

    Args:
        id (int): Thesis id
        name (str): Thesis name
        advisor (Optional[int]): Advisor id
        student (str): Student name
    """

    def __init__(self, id: int, name: str, advisor: Optional[int], student: str):
        self.id = id
        self.name = name
        self.advisor = advisor
        self.student = student

    def __str__(self):
        return f"Thesis {self.id}: {self.name}"

    def __repr__(self):
        return self.__str__()


class AssignmentResponse(BaseModel):
    fitness: float
    assignment: List[int]


class ThesisInfo(BaseModel):
    thesis: str
    student: str
    similarity: float


class TeacherAssigment(BaseModel):
    teacher: str
    theses: List[ThesisInfo]


class AssignmentNew(BaseModel):
    teachers: List[TeacherAssigment]
    total_similarity: float
