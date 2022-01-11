# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 07:56:38 2022

@author: StillScripts
"""

''' Imports '''
from enum import Enum
import random
from faker import Faker
from datetime import datetime
fake = Faker()

''' CLASSES AND FUNCTIONS '''

''' Blueprint for possible choices when running the program '''
class Actions(Enum):
    GET_ATTRIBUTES = 0
    GENERATE_SAMPLE_DATA = 1

''' Blueprint for running all the possible special functions '''
class Magic(Enum):
    DEFAULT = 0
    RACE_TIMES = 1 # Used for generating race times
    GET_DAY = 2 # Used for generating race day
    PROCESS_TEAM_MEMBERS = 3 # Used for saving the ids of specific members


''' Blueprint for the possible data types to use '''
class Types(Enum):
    INT_INCREMENT = 0 # An AUTO_INCREMENT ID
    INT_FOREIGN_KEY = 1 # A FOREIGN_KEY referencing an AUTO_INCREMENT ID
    INT = 2 # INT within a value range
    DECIMAL = 3 # DECIMAL within a value range
    BOOLEAN = 4 # TRUE/FALSE
    VARCHAR = 5 # Random string of text within a text length range
    TEXT = 6 # Random string of text within a text length range
    FIRST_NAME = 7 # Random first name
    LAST_NAME = 8 # Random last name
    COUNTRY = 9 # Random country
    ADDRESS = 10 # Random street address
    CITY = 11 # Random town
    STATE = 12 # Random statecode
    PHONE = 13 # Random phone number
    EMAIL = 14 # Random email address
    DATE = 15 # Random date
    SINGLE = 16 # Single value
    WILDCARD = 17 # Ordered set of values to use
    WILDCARD_RANDOM = 18 # Random list of values to use
    CODE_ID = 19 # Wildcard + index number
    MAGIC = 20 # Pass in a custom function which uses the index to do something 

    
''' Fields for an attribute in a table '''
class Attribute: 
    def __init__(self, data_type, null_status, limit=1, wildcard_values=[]):
        self.data_type = data_type
        self.null_status = null_status
        self.limit = limit
        self.wildcard_values = wildcard_values

 
''' 
    Save time by converting CREATE TABLE body into a
    default schema using the Attributes class 
'''
def create_attributes(table_name):
    schema = {} # Store the schema in this dictionary
    query_body = input("Paste your existing CREATE TABLE body: ")
    lines = query_body.split(",") # Create list of query lines
    for line in lines: # Iterate through lines
        key = "" # Store the attribute key
        value = "Attribute(Types" # Store the value as a string
        limit = "" # Store the attribute number
        get_key = False # Handle whether to record key
        for char in line: # Iterate through characters in the query to get key
            if get_key and char != "`":
                key += char
            if char == "`":
                get_key = not get_key
            if char.isdigit():
                limit += char
                null_status = True
        if ("AUTO_INCREMENT" in line.upper()):
            value += ".INT_INCREMENT"
        if ("NOT NULL" in line.upper()):
            null_status = False
        value += ", {}, {}, [])".format(str(null_status), limit)
        schema[key] = value
    print(table_name + " = {")
    for key in schema.keys():
        if len(key) > 0:
            print("    '{}': {},".format(key, schema[key]))
    print("}")
    

''' Generate a random int with a certain number of digits'''
def int_gen(digits):
    rand_int = random.randint(1*digits, 10**digits)
    return rand_int


''' Generate a random decimal with a certain number of digits and decimals '''
def dec_gen(limit, digits):
    rand_dec = random.random() * 10**digits
    return round(rand_dec, limit)


''' Handle magic functions  '''
def handle_magic(index=0, magic=Magic.DEFAULT, data_list=[]):
    if magic == Magic.RACE_TIMES:
        return create_time(index)
    elif magic == Magic.GET_DAY:
        return create_day(index)
    elif magic == Magic.PROCESS_TEAM_MEMBERS:
        return process_team_members(data_list)
    else:
        return data_list

''' Use the attributes of the column to generate sample value '''
def generate_value_for_column(column, index):
    value = "DEFAULT" # Default value
    if column.null_status and random.random() > 0.8:
        value = "EMPTY_PLACEHOLDER_VALUE" # Random NULL Value (20% likelihood)
    else:
        dt = column.data_type # The data type
        if dt == Types.INT_INCREMENT:
            value = index + 1 # increment by 1
        elif dt == Types.INT_FOREIGN_KEY:
            value = random.randint(1, column.limit)
        elif dt == Types.INT:
            value = int_gen(column.limit) # random int
        elif dt == Types.DECIMAL:
            value = dec_gen(2, column.limit) # random decimal
        elif dt == Types.BOOLEAN:
            value = random.random() < 0.5  # randomly True/False
        elif dt == Types.VARCHAR:
            value = fake.text(max_nb_chars=column.limit) # text within VARCHAR limit
        elif dt == Types.TEXT:
            value = fake.text(max_nb_chars=500) # 500 characters of text
        elif dt == Types.FIRST_NAME:
            value = fake.name().split(" ")[0] # realistic first name
        elif dt == Types.LAST_NAME:
            value = fake.name().split(" ")[1] # realistic last name
        elif dt == Types.ADDRESS:
            value = fake.street_address() # realistic street address
        elif dt == Types.CITY:
            value = fake.city() # realistic city
        elif dt == Types.STATE:
            value = fake.country_code() # realistic state code
        elif dt == Types.PHONE:
            value = "(02) "+ "{}".format(int_gen(8)) # realistic phone number
        elif dt == Types.EMAIL:
            value = fake.free_email() # realistic email
        elif dt == Types.DATE:
            value = fake.date_between_dates(
                date_start=datetime(2021,1,1), 
                date_end=datetime(2021,12,31)) # date within range
        elif dt == Types.SINGLE:
            value = column.wildcard_values[0] # use the single wildcard value
        elif dt == Types.WILDCARD:
            value = column.wildcard_values[index] # use each wildcard value in order
        elif dt == Types.WILDCARD_RANDOM:
            index_num = random.randint(1, len(column.wildcard_values)) # randomly use wildcard values
            value = column.wildcard_values[index_num-1]  
        elif dt == Types.CODE_ID:
            value = "{}-{}".format(column.wildcard_values[0], index+1)
        elif dt == Types.MAGIC:
            value = handle_magic(index, column.wildcard_values)   
    return value


''' Write the sample INSERT INTO query to a file '''
def create_query_file(table_name, table_keys, sample_data):
    # Convert '"'  and "'" into '`'
    table_keys = str(table_keys).replace('"', '`').replace("'", "`")  
    # Create the INSERT INTO statement as a string
    statement = "INSERT INTO `{}` {} \n VALUES \n {}".format(table_name, table_keys, sample_data)
    # Remove "[" and "]" characters
    statement = statement.replace("[", "").replace("]", "")
    # Convert the EMPTY_PLACEHOLDER_VALUE to NULL for SQL
    statement = statement.replace("'EMPTY_PLACEHOLDER_VALUE'", "NULL")
    with open('{}.txt'.format(table_name), 'w') as f:
        f.write(statement)


''' 
  Generate data for an INSERT INTO query.
  Filename is the Table name. 
  Schema is the attributes key names and data types. 
  Limit is the amount of rows to generate.
'''
def generate_sample_data(table_name, schema, limit, apply_process=False, magic=Magic.DEFAULT):
    index = 0 # Track index value of row
    data_list = [] # Store all sample data for table
    # Create as many values as the set limit
    while index < limit:
        keys = schema.keys() # Access the keys of the schema
        row = {} # Store the current row data
        row_index = 0
        for key in keys:
            # Use function to generate the appropriate value
            value = generate_value_for_column(schema[key], index)
            row[key] = value # Add value to row
            row_index += 1
        data_list.append(row) # Add row to table
        index += 1 # Go to next row
    if apply_process:
        # Call the method used to apply a special process
        data_list = handle_magic(0, magic, data_list)
    # Convert the table keys and sample data into tuple
    table_keys = [tuple(schema.keys())]
    sample_data = [tuple(row.values()) for row in data_list] 


    '''print(table_name) # Display table name
    print(table_keys) # Display table keys
    print(str(sample_data)) # Display the tuple data'''
    
    create_query_file(table_name, table_keys, sample_data)
    

       
''' 
    SCHEMA FOR TABLES!!! 
    Sample project is a sports event
    Tables needed include - 
'''
# Lists used in schemas
#coach_ids = [1, 14, 22, 24, 25, 26, 30, 36, 41, 42, 44, 46, 51, 54, 57, 61, 63, 70, 77, 85, 92, 99, 102, 109, 111, 113, 144, 149, 152, 155, 160, 163, 168, 172, 181, 183, 186, 189, 193, 201, 202, 205, 206, 226, 238, 247, 258, 259, 261, 267, 269, 274, 275, 277, 281, 283, 290, 299, 310, 311, 312, 331, 347, 355, 358, 359, 360, 367, 378, 382, 383, 387, 394, 395, 405, 407, 411, 413, 415, 418, 424, 425, 429, 431, 436, 447, 449, 453, 459, 463, 468, 471, 478, 479, 484, 489, 501, 505, 506, 511, 514, 528, 534, 539, 553, 555, 559, 580, 582, 585, 586, 600, 601, 610, 612, 613, 617, 622, 623, 624, 634, 635, 637, 643, 645, 649, 658, 659, 665, 670, 674, 676, 682, 684, 692, 693, 699, 707, 710, 711, 718, 733, 736, 749, 751, 754, 760, 765, 769, 775, 789, 794, 797, 811, 812, 819, 823, 829, 837, 854, 855, 858, 859, 860, 862, 869, 875, 876, 877, 881, 885, 893, 900, 902, 906, 910, 921, 923, 926, 929, 935, 936, 947, 962, 975, 985, 988, 991]
coach_ids = [1, 8, 23, 27, 30, 35, 37, 39, 40, 42, 48, 55, 61, 66, 71, 88, 97]
medical_ids = [7, 14, 19, 20, 26, 32, 34, 43, 46, 49, 52, 54, 67, 69, 73, 79, 84, 85, 87, 98, 99]
swimmer_ids = [2, 6, 9, 13, 18, 31, 33, 36, 56, 57, 68, 78, 82, 83, 89, 91]
countries = ['Anguilla', 'Antigua and Barbuda', 'Australia', 'Bahamas', 'Bangladesh', 'Barbados', 'Belize', 'Bermuda', 'Botswana', ' Britain', 'British Virgin Islands', 'Brunei', 'Cameroon', 'Canada', 'Cayman Islands', 'Cook Islands', 'Cyprus', 'Dominica', 'Falkland Islands', 'Fiji', 'Ghana', 'Gibraltar', 'Grenada', 'Guernsey', 'Guyana', 'India', 'Isle of Man', 'Jamaica', 'Jersey', 'Kenya', 'Kiribati', 'Lesotho', 'Malawi', 'Malaysia', 'Malta', 'Mauritius', 'Montserrat', 'Mozambique', 'Namibia', 'Nauru', 'New Zealand', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Ireland', 'Pakistan', 'Papua New Guinea', 'Rwanda', 'Saint Helena', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'Scotland', 'Seychelles', 'Sierra Leone', 'Singapore', 'Solomon Islands', 'South Africa', 'Sri Lanka', 'Swaziland', 'Tanzania', 'Tonga', 'Trinidad and Tobago', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Vanuatu', 'Wales', 'Zambia']
races = ['Heat 1','Heat 2','Heat 3','Heat 4','Semi-Final 1','Semi-Final 2']
event_names = ["800m Freestyle - Men","800m Freestyle - Women","1500m Freestyle - Men","1500m Freestyle - Women","4 x 100m Freestyle Relay - Men", "4 x 100m Freestyle Relay - Women", "4 x 100m Medley Relay - Men","4 x 100m Medley Relay - Women", "4 x 200m Freestyle Relay - Men","4 x 200m Freestyle Relay - Women"]
qualifying_times = ["8:01:22","8:31.25","15:12.97","16:10.88","3:16.37","3:40.00","3:34.47","4:00.57","7:10.36","7:52.45"]

#COACH
COACH = {
    'TeamMemberID': Attribute(Types.WILDCARD, False, 0, coach_ids),
    'CertificationLevel': Attribute(Types.WILDCARD_RANDOM, False, 0, [1,2,3,4,5]),
    'CertificationDate': Attribute(Types.DATE, False, 0, []),
    'WWCCheckDate': Attribute(Types.DATE, False, 0, []),
    'IsHeadCoach': Attribute(Types.WILDCARD_RANDOM, False, 0, ["EMPTY_PLACEHOLDER_VALUE"]),
}

# COMMONWEALTH_GAME
COMMONWEALTH_GAME = {
    "Year": Attribute(Types.WILDCARD, False, None, [2022]),
    "Country": Attribute(Types.WILDCARD, False, None, ["England"]),
    "City": Attribute(Types.WILDCARD, False, None, ["Birmingham"])
}

# EVENT
EVENT = {
    'EventID': Attribute(Types.INT_INCREMENT, False, 8, []),
    'Year': Attribute(Types.WILDCARD_RANDOM, False, 4, [2022]),
    'Name': Attribute(Types.WILDCARD, False, 0, event_names),
    'MinimumQualifyingTime': Attribute(Types.WILDCARD, False, 0, qualifying_times),
}

# EVENT_REGISTRATION
EVENT_REGISTRATION = {
    'Event': Attribute(Types.WILDCARD_RANDOM, False, 0, [1,2,3,4,5,6,7,8,9,10]),
    'Swimmer': Attribute(Types.WILDCARD_RANDOM, False, 0, swimmer_ids),
    'QualifyingTime': Attribute(Types.WILDCARD_RANDOM, False, 0, ['25.62','25.05','25.32','26.79','23.55']),
    'QualifyingDate': Attribute(Types.DATE, False),
    'QualifyingCompetition': Attribute(Types.WILDCARD_RANDOM, False, 0, ['Pan Pacific','European Junior Swimming Championships','World Aquatics Championships']),
}

# GAMES_REGISTRATION
GAMES_REGISTRATION = {
    'Country': Attribute(Types.WILDCARD, False, 0, countries),
    'Year': Attribute(Types.WILDCARD_RANDOM, False, 0, [2022])
}

# MEDICAL
MEDICAL = {
    'TeamMemberID': Attribute(Types.WILDCARD, False, 0, medical_ids),
    'Qualification': Attribute(Types.WILDCARD_RANDOM, False, 6, ['MD','MBBS','M.Med']),
    'Specialisation': Attribute(Types.WILDCARD_RANDOM, True, 20, ['Orthopaedics','Surgery']),
    'QualificationDate': Attribute(Types.DATE, False),
    'IsChiefMedicalOfficer': Attribute(Types.DATE, False),
}

# POOL
POOL = {
    'PoolID': Attribute(Types.INT_INCREMENT, False, 8, []),
    'Name': Attribute(Types.WILDCARD, False, 100, ["Competition Pool","Training Pool","Program Pool","Diving Pool"]),
    'LaneCount': Attribute(Types.WILDCARD, False, 2, [10, 8, 7, "EMPTY_PLACEHOLDER_VALUE"]),
    'Length': Attribute(Types.WILDCARD, False, 5, [50, 50, 25, 33]),
}

# RACE

''' Generate time in an ultra-custom way '''
def create_time(index):
    if 20 <= index < 40:
        index -= 20
    if 40 <= index < 60:
        index -= 40
    hours = 10
    mins = "00"
    remainder = index % 4
    if remainder:
        mins = "{}".format(remainder * 15)
    else:
        mins = "00"
    if 4 <= index < 8:
        hours += 1
    elif 8 <= index < 12:
        hours += 2
    elif  12 <= index < 16:
        hours += 3
    elif  16 <= index < 20:
        hours += 4
    return "{}:{}:00".format(hours, mins)

''' Generate day in an ultra-custom way '''
def create_day(index):
    if index < 20:
        return 1
    elif 20 <= index < 40:
        return 2
    elif 40 <= index < 60:
        return 3

RACE = {
    'RaceID': Attribute(Types.INT_INCREMENT, False, 8, []),
    'Event': Attribute(Types.WILDCARD_RANDOM, False, 8, [1,2,3,4,5,6,7,8,9,10]),
    'Name': Attribute(Types.WILDCARD_RANDOM, False, 20, races),
    'IsFinal': Attribute(Types.WILDCARD_RANDOM, False, 0, ["EMPTY_PLACEHOLDER_VALUE"]),
    'Day': Attribute(Types.MAGIC, False, 0, Magic.GET_DAY),
    'StartTime': Attribute(Types.MAGIC, False, 0, Magic.RACE_TIMES),
    'Pool': Attribute(Types.WILDCARD_RANDOM, False, 8, [1]),
}

#RACE_RESULT
RACE_RESULT = {
    'Race': Attribute(Types.INT_FOREIGN_KEY, False, 60),
    'Swimmer': Attribute(Types.WILDCARD_RANDOM, False, 0, swimmer_ids),
    'Lane': Attribute(Types.INT_FOREIGN_KEY, False, 10),
    'RecordedTime': Attribute(Types.DECIMAL, False, 2),
    'Place': Attribute(Types.INT_FOREIGN_KEY, False, 10)
}


#SWIMMER
SWIMMER = {
    'TeamMemberID': Attribute(Types.WILDCARD, False, 0, swimmer_ids),
    'DateOfBirth': Attribute(Types.DATE, False, 0, []),
    'Coach': Attribute(Types.WILDCARD_RANDOM, False, 0, coach_ids),
    'IsTeamLeader': Attribute(Types.WILDCARD_RANDOM, False, 0, ["EMPTY_PLACEHOLDER_VALUE"]),
}

#TEAM
TEAM = {
    'Country': Attribute(Types.WILDCARD, False, 0, countries),
    'PostalAddress': Attribute(Types.ADDRESS, False, 0, []),
    'PhoneContact': Attribute(Types.PHONE, False, 0, []),
}

#TEAM_MEMBER
''' Special function to process team member data '''
def process_team_members(data_list):
    coaches_list = []
    medical_list = []
    swimmers_list = []
    index = 0
    for row in data_list:
        if row['MembershipType'] == "Coach":
            coaches_list.append(row['TeamMemberID'])
        elif row['MembershipType'] == "Medical":
            medical_list.append(row['TeamMemberID'])
        elif row['MembershipType'] == "Swimmer":
            swimmers_list.append(row['TeamMemberID'])
        elif row['MembershipType'] == "TeamManager":
            data_list[index]['IsTeamManager'] = True
        index += 1
    print("coach_ids = {}".format(str(coaches_list)))
    print("medical_ids = {}".format(str(medical_list)))
    print("swimmer_ids = {}".format(str(swimmers_list)))
    return data_list

TEAM_MEMBER = {
    'TeamMemberID': Attribute(Types.INT_INCREMENT, False, 8, []),
    'Country': Attribute(Types.WILDCARD_RANDOM, False, 20, countries),
    'FirstName': Attribute(Types.FIRST_NAME, False, 20, []),
    'LastName': Attribute(Types.LAST_NAME, False, 20, []),
    'Phone': Attribute(Types.PHONE, False, 10, []),
    'Address': Attribute(Types.ADDRESS, False, 40, []),
    'City': Attribute(Types.CITY, False, 20, []),
    'State': Attribute(Types.STATE, False, 0, []),
    'Postcode': Attribute(Types.INT, False, 4, []),
    'Email': Attribute(Types.EMAIL, False, 0, []),
    'IsTeamManager': Attribute(Types.WILDCARD_RANDOM, False, 0, ["EMPTY_PLACEHOLDER_VALUE"]),
    'MembershipType': Attribute(Types.WILDCARD_RANDOM, False, 1, ["Team Manager", "Swimmer", "General Staff", "Coach", "Medical"]),
}

STUDENT = {
    'FirstName': Attribute(Types.FIRST_NAME, False, 0, []),
    'LastName': Attribute(Types.LAST_NAME, False, 0, []),
    'Address': Attribute(Types.ADDRESS, False, 0, []),
    'City': Attribute(Types.CITY, False, 0, []),
    'State': Attribute(Types.STATE, False, 0, []),
    'Postcode': Attribute(Types.INT, False, 4, []),
    'Phone': Attribute(Types.PHONE, False, 0, []),
    'Email': Attribute(Types.EMAIL, False, 0, [])
}

COUNTRY_TEAM = {
    'GamesID': Attribute(Types.INT_INCREMENT, False, 8, []),
    'Country': Attribute(Types.WILDCARD_RANDOM, False, 20, countries),
    'LastName': Attribute(Types.LAST_NAME, False, 20, []),
    'FirstName': Attribute(Types.FIRST_NAME, False, 20, []),
    'ContactMobile': Attribute(Types.PHONE, False, 10, []),
    'Address': Attribute(Types.ADDRESS, False, 40, []),
    'City': Attribute(Types.CITY, False, 20, []),
    'State': Attribute(Types.STATE, False, 0, []),
    'Postcode': Attribute(Types.INT, False, 4, []),
    'Email': Attribute(Types.EMAIL, False, 0, [])
}
    


''' Function to run the program (2 Options for the action) '''
def run(action, table_name, 
        schema={"Year": Attribute(Types.WILDCARD, False, None, [2022])}, 
        limit=1, apply_process=False, magic=Magic.DEFAULT):
    if action == Actions.GET_ATTRIBUTES:
        create_attributes(table_name)
    elif action == Actions.GENERATE_SAMPLE_DATA:
        generate_sample_data(table_name, schema, limit, apply_process, magic)



''' RUN the program here '''
#run(Actions.GET_ATTRIBUTES, "RACE_RESULT")
#run(Actions.GENERATE_SAMPLE_DATA, "TEAM_MEMBER", TEAM_MEMBER, 100, True, Magic.PROCESS_TEAM_MEMBERS)
#run(Actions.GENERATE_SAMPLE_DATA, "SWIMMER", SWIMMER, 50)

run(Actions.GENERATE_SAMPLE_DATA, "COUNTRY_TEAM", COUNTRY_TEAM, len(countries))