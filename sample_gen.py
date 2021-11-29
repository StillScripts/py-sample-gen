# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 13:52:54 2021

@author: @StillScripts
"""

from enum import Enum
import random
import string
from faker import Faker
fake = Faker()


def swap_quotes():
    stringA = input(": ")
    reset = ""
    for i in stringA: 
        if i == "`":
            reset += '"'
        else: 
            reset += i
    print(reset)

def int_gen(length):
    rand_int = random.randint(1, 10**length)
    return rand_int

def dec_gen(digits):
    rand_dec = random.random() * 50
    return round(rand_dec, digits)
    
def sample_generation(filename, schema, length):
    start = 0
    data_array = []
    while start < length:
        keys = schema.keys()
        row = {}
        rand_num = random.random()
        for i in keys:
            value = 'DEFAULT'
            if schema[i][1] and rand_num>0.75:
                value = None
            else:
                if schema[i][0] == Types.FOREIGN_KEY:
                    value = random.randint(1, schema[i][2])
                elif schema[i][0] == Types.BOOLEAN:
                    if rand_num>0.5:
                        value = True
                    else:
                        value = False
                elif schema[i][0] == Types.INT:
                    value = int_gen(schema[i][2])
                elif schema[i][0] == Types.DECIMAL:
                    value = dec_gen(schema[i][2])
                elif schema[i][0] == Types.VARCHAR:
                    value = fake.text(max_nb_chars=schema[i][2])
                elif schema[i][0] == Types.TEXT:
                    value = fake.text(max_nb_chars=schema[i][2])
                elif schema[i][0] == Types.DATE:
                    value = fake.date()
                elif schema[i][0] == Types.FIRST_NAME:
                    value = fake.name().split(" ")[0]
                elif schema[i][0] == Types.LAST_NAME:
                    value = fake.name().split(" ")[1]
                elif schema[i][0] == Types.INT_INCREMENT:
                    value = start + 1
                elif schema[i][0] == Types.ADDRESS:
                    value = fake.street_address()
                elif schema[i][0] == Types.CITY:
                    value = fake.city()
                elif schema[i][0] == Types.STATE:
                    if rand_num < 0.5:
                        value = "QLD"
                    else:
                        value = "NSW"
                elif schema[i][0] == Types.POSTCODE:
                    if rand_num < 0.5:
                        value = 4000 + int_gen(3)
                    else:
                        value = 2000 + int_gen(3)
                elif schema[i][0] == Types.PHONE:
                    value = "(02) "+ "{}".format(int_gen(8))
                elif schema[i][0] == Types.EMAIL:
                    value = fake.free_email()
                elif schema[i][0] == Types.CREDIT:
                    if rand_num < 0.33:
                        value = 192
                    elif 0.33 < rand_num < 0.66:
                        value = 288
                    else:
                        value = 192
                elif schema[i][0] == Types.ROOM_CODE:
                    building = row["Building"]
                    floor = row["Floor"]
                    value = "{}-{}-{}".format(building, floor, random.randint(1, 20))
                elif schema[i][0] == Types.FUNCTION:
                    value = "It is used for {}".format(fake.text(max_nb_chars=80))
                elif schema[i][0] == Types.UNIT_CODE:
                    text = ''.join(random.choice(string.ascii_uppercase) for i in range(3))
                    num = ''.join(random.choice(string.digits) for i in range(4))
                    value = "{}{}".format(text, num)                    
                elif schema[i][0] == Types.WILDCARD:
                    value = schema[i][2][start]
                elif schema[i][0] == Types.WILDCARD_RANDOM:
                    index_num = random.randint(1, len(schema[i][2]))
                    value = schema[i][2][index_num-1]
            row[i] = value
        data_array.append(row)
        start += 1
    result = [tuple(row.values()) for row in data_array]
    print(filename)
    print(str(result))
    with open('{}.txt'.format(filename), 'w') as f:
        f.write(str(result))

            
    
class Types(Enum):
    FOREIGN_KEY = 0
    BOOLEAN = 1
    INT = 2
    VARCHAR = 3
    TEXT = 4
    DATE = 5
    FIRST_NAME = 6
    LAST_NAME = 7
    INT_INCREMENT = 8
    ADDRESS = 9
    CITY = 10
    STATE = 11
    POSTCODE = 12
    PHONE = 13
    EMAIL = 14
    CREDIT = 15
    ROOM_CODE = 16
    FUNCTION = 17
    UNIT_CODE = 18
    WILDCARD = 19
    WILDCARD_RANDOM = 20
    DECIMAL = 21
    

assessment = {
    "AssessmentID": [Types.INT_INCREMENT, False],
    "UnitOfferingID": [Types.FOREIGN_KEY, False, 25],
    "AssementName": [Types.VARCHAR, False, 40],
    "AssessmentDescription": [Types.TEXT, False, 100],
    "DueDate": [Types.DATE, False],
    "PossibleMarks": [Types.INT, False, 2]
}
#sample_generation("assessment", assessment, 30) 

campus = {
    "CampusID": [Types.INT_INCREMENT, False],
	"StreetAddress": [Types.ADDRESS, False],
	"City": [Types.CITY, False],
	"State": [Types.STATE, False],
	"Postcode": [Types.POSTCODE, False, 4],
	"PhoneHelpline": [Types.PHONE, False],
}
#sample_generation("campus", campus, 15) 

course = {
    "CourseCode": [Types.INT_INCREMENT, False],
	"CourseName": [Types.WILDCARD, False, ["Maths", "Biology", "Geology", "Medicine", "Computer Science", "Information Technology", "Engineering", "Counselling", "Law", "Environmental Science"]],
	"CreditPoints": [Types.CREDIT, False],
	"Notes": [Types.TEXT, True, 100],
}
#sample_generation("course", course, len(course["CourseName"][2])) 

course_enrolment = {
    "StudentID": [Types.FOREIGN_KEY, False, 85],
    "CourseCode": [Types.FOREIGN_KEY, False, 9],
    "EnrolmentDate": [Types.DATE, False],
    "CurrentStatus": [Types.WILDCARD_RANDOM, False, ["Complete", "Enrolled", "Deferred"]]
}
#sample_generation("course_enrolment", course_enrolment, 80) 

room = {
    "RoomID": [Types.INT_INCREMENT, False],
    "Building": [Types.WILDCARD_RANDOM, False, ["A", "B", "C", "D"]],
    "Floor": [Types.WILDCARD_RANDOM, False, [1, 2, 3, 4, 5]],
    "RoomCode": [Types.ROOM_CODE, False],
    "Function": [Types.FUNCTION, False],
    "CampusID": [Types.FOREIGN_KEY, False, 14],
}
#sample_generation("room", room, 30) 

student = {
    "StudentID": [Types.INT_INCREMENT, False],
	"FirstName": [Types.FIRST_NAME, False],
	"LastName": [Types.LAST_NAME, False],
	"StreetAddress": [Types.ADDRESS, False],
	"City": [Types.CITY, False],
	"State": [Types.STATE, False],
	"Postcode": [Types.POSTCODE, False, 4],
	"Email": [Types.EMAIL, False],
}
#sample_generation("student", student, 50) 

student_assessment = {
    "AssessmentID": [Types.FOREIGN_KEY, False, 29],
    "StudentID": [Types.FOREIGN_KEY, False, 89],
    "DateSubmitted": [Types.DATE, False],
    "DaysExtension": [Types.INT, True, 1],
    "MarksAwarded": [Types.DECIMAL, True, 2] 
}
#sample_generation("student-assessment", student_assessment, 200) 

teacher = {
    "StaffID": [Types.INT_INCREMENT, False],
	"FirstName": [Types.FIRST_NAME, False],
	"LastName": [Types.LAST_NAME, False],
	"Email": [Types.EMAIL, False],
	"Phone": [Types.PHONE, True],
	"OfficeID": [Types.FOREIGN_KEY, True, 29]
}
#sample_generation("teacher", teacher, 12) 

unit = {
	"UnitCode": [Types.UNIT_CODE, False],
	"UnitName": [Types.VARCHAR, False, 20],
	"Description": [Types.TEXT, False, 100],
	"CourseCode": [Types.FOREIGN_KEY, False, 9],
}
#sample_generation("unit", unit, 11) 

unit_offering = {
    "UnitOfferingID": [Types.INT_INCREMENT, False],
    "UnitCode": [Types.WILDCARD_RANDOM, False, ['ICC7121', 'WVD2142', 'MYF2875', 'YXW3245', 'RBT6140']],
    "Year": [Types.WILDCARD_RANDOM, False, [2014, 2015, 2016, 2017]],
    "Session": [Types.WILDCARD_RANDOM, False, [1, 2, 3]],
    "AssessorID": [Types.FOREIGN_KEY, False, 11]
}
#sample_generation("unit-offering", unit_offering, 26) 

unit_enrolment = {
    "StudentID": [Types.FOREIGN_KEY, False, 89],
    "UnitOfferingID": [Types.FOREIGN_KEY, False, 25],
    "EnrolmentType": [Types.WILDCARD_RANDOM, False, ["External", "On-Campus"]],
    "FinalGrade": [Types.WILDCARD_RANDOM, True, ["Fail", "Pass", "Credit", "Distinction", "High Distinction"]],
}
#sample_generation("unit-enrolment", unit_enrolment, 150) 

workshop = {
    "WorkshopID": [Types.INT_INCREMENT, False],
    "UnitOfferingID": [Types.FOREIGN_KEY, False, 25],
    "ClassroomID": [Types.FOREIGN_KEY, False, 29],
    "TeacherID": [Types.FOREIGN_KEY, False, 11],
    "DayOfWeek": [Types.WILDCARD_RANDOM, False, ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]],
    "ClassTimes": [Types.WILDCARD_RANDOM, False, ["10AM-12PM", "2PM-4PM", "3PM-5PM"]],
}
#sample_generation("workshop", workshop, 15) 

workshop_enrolment = {
    "WorkshopID": [Types.FOREIGN_KEY, False, 15],
    "StudentID": [Types.FOREIGN_KEY, False, 89],
}
#sample_generation("workshop-enrolment", workshop_enrolment, 50) 

#swap_quotes()