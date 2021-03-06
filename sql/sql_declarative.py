import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

"""
 This is an intended as a learning exercise for SQLAlchemy. This class structure 
 represents my personal academic year, and it's constraints and relationships 
 reflect that fact. eg.) Only one lecturer per course.
"""

Base=declarative_base()

class Person(Base):
    __tablename__='person'
    id=Column(Integer, primary_key=True)
    first_name=Column(String, nullable=False)
    last_name=Column(String, nullable=False)

# inherits from person, defines one to many relationship with lectures
class Lecturer(Person):
    __tablename__='lecturer'
    id=Column(None, ForeignKey('person.id'), primary_key=True)
    courses=relationship('Course')

# inherits from person, defines many to many relationship with courses
# using association table.
class Student(Person):
    __tablename__='student'
    id=Column(None, ForeignKey('person.id'), primary_key=True)
    student_id=Column(Integer, nullable=False, unique=True)
    courses=relationship('Course', secondary='student_course')

# 
class Course(Base):
    __tablename__='course'
    id=Column(String, primary_key=True)
    title=Column(String, nullable=False)
    desc=Column(String, nullable=False)
    semester=Column(Integer, nullable=False)
    lecturer_id=Column(Integer, ForeignKey('lecturer.id'))
    students=relationship('Student', secondary='student_course')
    lectures=relationship('Lecture')

# association table, resolves many to many relationship between student and course
class StudentCourse(Base):
    __tablename__='student_course'
    student_id=Column(Integer, ForeignKey('student.student_id'), primary_key=True)
    course_id=Column(String, ForeignKey('course.id'), primary_key=True)

class Lecture(Base):
    __tablename__='lecture'
    lecture_id=Column(Integer, primary_key=True)
    course_id=Column(String, ForeignKey('course.id'))
    class_room=Column(String, nullable=False)
    day=Column(String, nullable=False)
    time=Column(String, nullable=False)

engine=create_engine('sqlite:///my_year.db')

Base.metadata.create_all(engine)
