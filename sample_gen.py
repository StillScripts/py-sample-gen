# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 07:56:38 2022

@author: StillScripts
"""

''' Imports '''
from enum import Enum
import math
import random
from faker import Faker
from datetime import datetime
from datetime import date
my_date = date(2021, 3, 2)
fake = Faker()

''' CLASSES AND FUNCTIONS '''

''' Blueprint for possible choices when running the program '''
class Actions(Enum):
    GET_ATTRIBUTES = 0
    GENERATE_SAMPLE_DATA = 1

''' Blueprint for running all the possible special functions '''
class Magic(Enum):
    DEFAULT = 0
    GET_HEAT = 1 # Used for generating the race heat 
    GET_DAY = 2 # Used for generating race day
    GET_RACE_TIME = 3 # Used for generating race times
    GET_EVENT_ID = 4 # Used for generating eventID for race
    GET_TEAM= 5 # Used for getting the team
    GET_TEAM_ROLE = 6 # Used for team membership roles
    PROCESS_TEAM_MEMBERS = 7 # Used for saving the ids of specific members
    PREVENT_DUPLICATES = 8 # Used for preventing duplicate composite keys


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
    if magic == Magic.GET_HEAT:
        return create_heat(index)
    elif magic == Magic.GET_DAY:
        return create_day(index)
    elif magic == Magic.GET_RACE_TIME:
        return create_time(index)
    elif magic == Magic.GET_EVENT_ID:
        return select_event(index)
    elif magic == Magic.GET_TEAM:
        return create_membership(index, False)
    elif magic == Magic.GET_TEAM_ROLE:
        return create_membership(index, True)
    elif magic == Magic.PROCESS_TEAM_MEMBERS:
        return process_team_members(data_list)
    elif magic == Magic.PREVENT_DUPLICATES:
        return prevent_duplicates(index)
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
            value = random.randint(1, column.limit) # use foreign key randomly
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
                date_end=datetime(2021,12,31)).strftime('%Y-%m-%d') # date within range
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
            value = handle_magic(index, column.wildcard_values) # fun the magic function 
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
    with open('{}.sql'.format(table_name), 'w') as f:
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

coach_ids = [71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 286, 287, 288, 292, 298, 300, 301, 303, 307, 309, 310, 313, 315, 316, 318, 324, 332, 338, 340, 341, 347, 349, 357, 358, 359, 367, 368, 370, 378, 379, 384, 386, 387, 392, 393, 396, 400]
medical_ids = [211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 283, 290, 291, 293, 294, 295, 297, 299, 308, 311, 312, 322, 323, 326, 328, 329, 342, 344, 346, 351, 353, 354, 355, 356, 360, 366, 369, 372, 373, 377, 381, 385, 394, 397]
swimmer_ids = [141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 282, 284, 285, 296, 302, 304, 305, 306, 314, 321, 327, 333, 335, 339, 343, 361, 362, 371, 375, 380, 383, 389, 390, 399]
countries = ['Anguilla', 'Antigua and Barbuda', 'Australia', 'Bahamas', 'Bangladesh', 'Barbados', 'Belize', 'Bermuda', 'Botswana', ' Britain', 'British Virgin Islands', 'Brunei', 'Cameroon', 'Canada', 'Cayman Islands', 'Cook Islands', 'Cyprus', 'Dominica', 'Falkland Islands', 'Fiji', 'Ghana', 'Gibraltar', 'Grenada', 'Guernsey', 'Guyana', 'India', 'Isle of Man', 'Jamaica', 'Jersey', 'Kenya', 'Kiribati', 'Lesotho', 'Malawi', 'Malaysia', 'Malta', 'Mauritius', 'Montserrat', 'Mozambique', 'Namibia', 'Nauru', 'New Zealand', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Ireland', 'Pakistan', 'Papua New Guinea', 'Rwanda', 'Saint Helena', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'Scotland', 'Seychelles', 'Sierra Leone', 'Singapore', 'Solomon Islands', 'South Africa', 'Sri Lanka', 'Swaziland', 'Tanzania', 'Tonga', 'Trinidad and Tobago', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Vanuatu', 'Wales', 'Zambia']
approved = ['Pan Pacific','European Junior Swimming Championships','World Aquatics Championships']
event_names = ["800m Freestyle - Men","800m Freestyle - Women","1500m Freestyle - Men","1500m Freestyle - Women","4 x 100m Freestyle Relay - Men", "4 x 100m Freestyle Relay - Women", "4 x 100m Medley Relay - Men","4 x 100m Medley Relay - Women", "4 x 200m Freestyle Relay - Men","4 x 200m Freestyle Relay - Women"]
qualifying_times = ["8:01:22","8:31.25","15:12.97","16:10.88","3:16.37","3:40.00","3:34.47","4:00.57","7:10.36","7:52.45"]

#COACH
COACH = {
    'TeamMemberID': Attribute(Types.WILDCARD, False, 0, coach_ids),
    'CertificationLevel': Attribute(Types.WILDCARD_RANDOM, False, 0, [1,2,3,4,5]),
    'CertificationDate': Attribute(Types.DATE, False, 0, []),
    'WWCCheckDate': Attribute(Types.DATE, False, 0, [])
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
    'Year': Attribute(Types.SINGLE, False, 0, [2022]),
    'Name': Attribute(Types.WILDCARD, False, 0, event_names),
    'MinimumQualifyingTime': Attribute(Types.WILDCARD, False, 0, qualifying_times),
    'IsRelay': Attribute(Types.SINGLE, False, 0, [False])
}

# EVENT_REGISTRATION
EVENT_REGISTRATION = {
    'Event': Attribute(Types.INT_FOREIGN_KEY, False, 10, []),
    'Swimmer': Attribute(Types.WILDCARD_RANDOM, False, 0, swimmer_ids),
    'QualifyingCompetition': Attribute(Types.INT_FOREIGN_KEY, False, 3, []),
    'QualifyingTime': Attribute(Types.WILDCARD_RANDOM, False, 0, ['25.62','25.05','25.32','26.79','23.55']),
    'QualifyingDate': Attribute(Types.DATE, False),
}

# GAMES_REGISTRATION
GAMES_REGISTRATION = {
    'Team': Attribute(Types.WILDCARD, False, 0, list(range(1,len(countries)+1))),
    'Year': Attribute(Types.SINGLE, False, 0, [2022])
}

# MEDICAL
MEDICAL = {
    'TeamMemberID': Attribute(Types.WILDCARD, False, 0, medical_ids),
    'Qualification': Attribute(Types.WILDCARD_RANDOM, False, 6, ['MD','MBBS','M.Med']),
    'Specialisation': Attribute(Types.WILDCARD_RANDOM, True, 20, ['Orthopaedics','Surgery']),
    'QualificationDate': Attribute(Types.DATE, False),
}

# NATIONAL_TEAM
NATIONAL_TEAM = {
    'NationalTeamID': Attribute(Types.INT_INCREMENT, False, 8, []),
    'Country': Attribute(Types.WILDCARD, False, 0, countries),
}

# POOL
POOL = {
    'PoolID': Attribute(Types.INT_INCREMENT, False, 8, []),
    'Name': Attribute(Types.WILDCARD, False, 100, ["Competition Pool","Training Pool","Program Pool","Diving Pool"]),
    'LaneCount': Attribute(Types.WILDCARD, False, 2, [10, 8, 7, "EMPTY_PLACEHOLDER_VALUE"]),
    'Length': Attribute(Types.WILDCARD, False, 5, [50, 50, 25, 33]),
}

#QUALIFYING_COMPETITION
QUALIFYING_COMPETITION = {
    'CompetitionID': Attribute(Types.INT_INCREMENT, False, 8, []),
    'Year': Attribute(Types.SINGLE, False, 0, [2021]),
    'Name': Attribute(Types.WILDCARD, False, 0, approved),
}


# RACE
''' Count a number down to a specific range '''
def count_down(number, decrement):
    if number > decrement:
        number -= decrement
        return count_down(number, decrement)
    else: 
        return number

''' Generate the id for the event '''
def select_event(index):
    # for heats, go up 1 every 4
    if index < 40:
        return math.ceil((index+1)/4)
    # for semi finals, go 1 very 2, 
    elif 40 <= index <= 60:
        new_index = count_down(index+1,20)
        return math.ceil(new_index/2)
    # for finals go up 1 every time
    else:
        return count_down(index+1,10)

''' Generate the heat in an ultra-custom way '''
def create_heat(index):
    if index < 40:
        return "Heat {}".format(count_down((index+1), 4))
    elif 40 <= index < 60:
        return "Semi Final {}".format(count_down((index+1), 2))
    else: 
        return "Final"
    

''' Generate time in an ultra-custom way '''
def create_time(index):
    index = count_down(index, 20)
    hours = 10 + math.floor(index/4)
    mins = "00"
    remainder = index % 4
    if remainder:
        mins = "{}".format(remainder * 15)
    else:
        mins = "00"
    return "{}:{}:00".format(hours, mins)

''' Generate day in an ultra-custom way '''
def create_day(index):
    return math.ceil((index+1)/20)


RACE = {
    'RaceID': Attribute(Types.INT_INCREMENT, False, 8, []),
    'Event': Attribute(Types.MAGIC, False, 0, Magic.GET_EVENT_ID),
    'Heat': Attribute(Types.MAGIC, False, 0, Magic.GET_HEAT),
    'Day': Attribute(Types.MAGIC, False, 0, Magic.GET_DAY),
    'StartTime': Attribute(Types.MAGIC, False, 0, Magic.GET_RACE_TIME),
    'Pool': Attribute(Types.SINGLE, False, 0, [1]),
}

#RACE_RESULT
RACE_RESULT = {
    'RaceResultID': Attribute(Types.INT_INCREMENT, False, 8, []),
    'Race': Attribute(Types.INT_FOREIGN_KEY, False, 70),
    'Lane': Attribute(Types.INT_FOREIGN_KEY, False, 10),
    'RecordedTime': Attribute(Types.WILDCARD_RANDOM, False, 0, ['25.62','25.05','25.32','26.79','2:23.55', '46.88', '1:33.12', '28.32']),
    'Place': Attribute(Types.INT_FOREIGN_KEY, False, 10),
    'Medal': Attribute(Types.SINGLE, False, 0, ["EMPTY_PLACEHOLDER_VALUE"])
}


#SWIMMER
SWIMMER = {
    'TeamMemberID': Attribute(Types.WILDCARD, False, 0, swimmer_ids),
    'Gender': Attribute(Types.WILDCARD_RANDOM, False, 0, ["Male", "Female"]),
    'DateOfBirth': Attribute(Types.DATE, False, 0, []),
    'Coach': Attribute(Types.WILDCARD_RANDOM, False, 0, coach_ids),
    'IsTeamLeader': Attribute(Types.SINGLE, False, 0, [False]),
}

#SWIMMER_RESULT
def prevent_duplicates(index):
    if index < 500:
        return index + 1
    else:
        return random.randint(1, 500)

SWIMMER_RESULT = {
    'Swimmer': Attribute(Types.WILDCARD_RANDOM, False, 8, swimmer_ids),
    'RaceResult': Attribute(Types.MAGIC, False, 8, Magic.PREVENT_DUPLICATES),
    'SwimmerTime': Attribute(Types.WILDCARD_RANDOM, False, 10, ['25.62','25.05','25.32','26.79','2:23.55', '46.88', '1:33.12', '28.32']),
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

''' Generate team or role in a custom way '''
def create_membership(index, role):
    if index < 70:
        if role:
            return "Team Manager"
        else: 
            return index + 1
    elif 70 <= index < 140:
        if role:
            return "Coach"
        else:
            return count_down((index+1), 70)
    elif 140 <= index < 210:
        if role:
            return "Swimmer"
        else:
            return count_down((index+1), 70)
    elif 210 <= index < 280:
        if role:
            return "Medical"
        else:
            return count_down((index+1), 70)
    elif index >= 280:
        if role:
            roles = ["Swimmer", "General", "Coach", "Medical"]
            return roles[random.randint(0, 3)]
        else:
            return random.randint(1, 70)


TEAM_MEMBER = {
    'TeamMemberID': Attribute(Types.INT_INCREMENT, False, 8, []),
    'Team': Attribute(Types.MAGIC, False, 0, Magic.GET_TEAM),
    'FirstName': Attribute(Types.FIRST_NAME, False, 0, []),
    'LastName': Attribute(Types.LAST_NAME, False, 0, []),
    'Phone': Attribute(Types.PHONE, False, 0, []),
    'Email': Attribute(Types.EMAIL, True, 0, []),
    'Address': Attribute(Types.ADDRESS, False, 0, []),
    'City': Attribute(Types.CITY, False, 0, []),
    'State': Attribute(Types.STATE, False, 0, []),
    'Postcode': Attribute(Types.INT, False, 5, []),
    'MembershipType': Attribute(Types.MAGIC, False, 0, Magic.GET_TEAM_ROLE),
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
    'Country': Attribute(Types.WILDCARD_RANDOM, False, 0, countries),
    'LastName': Attribute(Types.LAST_NAME, False, 0, []),
    'FirstName': Attribute(Types.FIRST_NAME, False, 0, []),
    'ContactMobile': Attribute(Types.PHONE, False, 0, []),
    'Address': Attribute(Types.ADDRESS, False, 0, []),
    'City': Attribute(Types.CITY, False, 0, []),
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
#run(Actions.GET_ATTRIBUTES, "SWIMMER_RESULT")
#run(Actions.GENERATE_SAMPLE_DATA, "TEAM_MEMBER", TEAM_MEMBER, 400, True, Magic.PROCESS_TEAM_MEMBERS)

run(Actions.GENERATE_SAMPLE_DATA, "SWIMMER_RESULT", SWIMMER_RESULT, 700)
