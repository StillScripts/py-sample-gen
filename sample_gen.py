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


''' Convert the ` character to the " character in a string '''
def swap_quotes(original):
    reset = ""
    for i in original: 
        if i == "`":
            reset += '"'
        else: 
            reset += i
    print(reset)

''' Generate a random integer within a range '''
def int_gen(limit):
    rand_int = random.randint(1, 10**limit)
    return rand_int

''' Generate a random decimal to a certain number of digits '''
def dec_gen(digits):
    rand_dec = random.random() * 50
    return round(rand_dec, digits)

''' 
  Generate data for an INSERT INTO query.
  Filename is the Table name. 
  Schema is the attributes key names and data types. 
  Limit is the amount of rows to generate.
'''
def generate_sample_data(filename, schema, limit):
    index = 0 # Track index value
    data_array = [] # Store data
    while index < limit:
        print("hey")
    
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

            

# All the possible data types to use for generation
class TypesZ(Enum):
    #UUID = 0
    INT_INCREMENT = 0 # An AUTO_INCREMENT ID
    INT_FOREIGN_KEY = 1 # A FOREIGN_KEY referencing an AUTO_INCREMENT ID
    BOOLEAN = 2 # TRUE/FALSE
    INT = 3 # INT within a value range
    DECIMAL = 4 # DECIMAL within a value range
    VARCHAR = 5 # Random string of text within a text length range
    TEXT = 6 # Random string of text within a text length range
    WILDCARD = 7 # Ordered set of values to use
    WILDCARD_RANDOM = 8 # Random list of values to use
    FIRST_NAME = 9 # Random first name
    LAST_NAME = 10 # Random last name
    ADDRESS = 11 # Random street address
    CITY = 12 # Random town
    PHONE = 13 # Random phone number
    EMAIL = 14 # Random email address

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
    
    
class Attribute: 
    def __init__(self, data_type: int, null_status: bool, limit: int, wildcard_values: list):
        self.data_type = data_type
        self.null_status = null_status
        self.limit = limit
        self.wildcard_values
        

hey = """CREATE TABLE IF NOT EXISTS COURSE (
	`CourseCode` INT(8) NOT NULL AUTO_INCREMENT,
	`CourseName` VARCHAR(50) NOT NULL,
	`CreditPoints` INT(3) NOT NULL,
	`Notes` TEXT DEFAULT NULL,
	PRIMARY KEY (`CourseCode`)
)"""
    
def num_input(question):
    val = 0
    num_chosen = False
    while not num_chosen:
        user_num = input(question)
        try:
            val = int(user_num)
            num_chosen = True
        except ValueError:
            print("Input is not a number, you must choose a number.")
    print(val)
    return val
            
# Parse the query text to determine the value
def get_initial_type(line):
    if "INT" in line.upper():
        return TypesZ.INT
    

# Allow user to make field wildcard and set its values
def let_field_be_wild(key, current_type):
    new_type = current_type
    values = []
    initial_check = input("Would you like to make {} a wildcard? (y/N)  ".format(key))
    if (len(initial_check) > 0 and initial_check[0].lower() == "y"):
        #continue
        random_check = input("Will this be an ordered or random wildcard? (o/R")
        if (len(random_check) > 0 and random_check.lower() == "o"):
            new_type = TypesZ.WILDCARD
        else: 
            new_type = TypesZ.WILDCARD_RANDOM
        amount = num_input("How many wildcard values would you like to add?  ")
        for i in range(amount):
            value = input("Enter wildcard value {}:  ".format(i))
            values.append(value)
        return (new_type, values) # Wilcard type with special values     
    else:
        return (current_type, []) # Non-wildcard
    
def sql_into_schema(query_body):
    schema = {} # Store the schema here
    lines = query_body.split(",") # Create list of query lines
    for line in lines: # Iterate through lines
        key = "" # Store the attribute key
        get_key = False # Handle whether to record key
        for char in line: # Iterate through characters in the query to get key
            if get_key:
                key += char
            if char == "`":
                get_key = not get_key
        null_status = True
        if ("NOT NULL" in line.upper()):
            null_status = False
        if ("AUTO_INCREMENT" in line.upper()):
            schema[key] = Attribute(TypesZ.INT_INCREMENT, null_status, 0, [])
        else: 
        # Get limits and wildcard values
            
            data_type, wildcard_values = let_field_be_wild(key, TypesZ.INT)
            limit = 100
            schema[key] = Attribute(data_type, null_status, limit, wildcard_values)
    print(schema)

            
            
            
        
    
    
# ass is a schema for the ass table
ass = {
       "Ass": Attribute(Types.INT_INCREMENT, True, 100, []),
       "Butt": Attribute(Types.INT_INCREMENT, False, 100, [])
}

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
    "MarksAwarded": [Types.DECIMAL, False, 2] 
}
sample_generation("student-assessment", student_assessment, 150) 

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