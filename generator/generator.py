# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 09:42:33 2022

@author: daniel
"""


import random
import uuid
from faker import Faker
from datetime import datetime
from enum import Enum
from example import magic_methods

fake = Faker()

''' Blueprint for possible choices when running the program '''
class Actions(Enum):
    GET_ATTRIBUTES = 0
    GENERATE_SAMPLE_DATA = 1


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
    UUID = 21 # Generate a random UUID.


''' Blueprint for running all the possible special functions '''
class Magic(Enum):
    DEFAULT = 0
    # Magic features can be anything...
    GET_HEAT = 1 # Used for generating the race heat 
    GET_DAY = 2 # Used for generating race day
    GET_RACE_TIME = 3 # Used for generating race times
    GET_EVENT_ID = 4 # Used for generating eventID for race
    GET_TEAM= 5 # Used for getting the team
    GET_TEAM_ROLE = 6 # Used for team membership roles
    PROCESS_TEAM_MEMBERS = 7 # Used for saving the ids of specific members
    PREVENT_DUPLICATES = 8 # Used for preventing duplicate composite keys


''' Generate a random int with a certain number of digits'''
def int_gen(digits):
    rand_int = random.randint(1*digits, 10**digits)
    return rand_int


''' Generate a random decimal with a certain number of digits and decimals '''
def dec_gen(limit, digits):
    rand_dec = random.random() * 10**digits
    return round(rand_dec, limit)


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
        # Magic is a custom feature that can be used for very specific data needs
        elif dt == Types.MAGIC:
            value = magic_methods.handle_magic(index, column.wildcard_values) # fun the magic function 
        elif dt == Types.UUID:
            value = str(uuid.uuid4())
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
        # Magic can be used for applying custom methods
        # Call the method used to apply a special process
        data_list = magic_methods.handle_magic(index, magic, data_list)
        
    # Convert the table keys and sample data into tuple
    table_keys = [tuple(schema.keys())]
    sample_data = [tuple(row.values()) for row in data_list] 

    '''print(table_name) # Display table name
    print(table_keys) # Display table keys
    print(str(sample_data)) # Display the tuple data'''
    
    create_query_file(table_name, table_keys, sample_data)
    
