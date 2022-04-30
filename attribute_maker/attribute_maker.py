# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 09:58:23 2022

@author: daniel
"""

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
    # Use print to display the generated Attribute object
    print(table_name + " = {")
    for key in schema.keys():
        if len(key) > 0:
            print("    '{}': {},".format(key, schema[key]))
    print("}")
    
