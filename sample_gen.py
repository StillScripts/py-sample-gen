# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 13:52:54 2021

@author: danie
"""

from enum import Enum
import random
import pandas as pd
import numpy as np
import string
from faker import Faker
fake = Faker()


def int_gen(length, existing_ints):
    rand_int = random.randint(1, 10**length)
    return rand_int
    
def sample_generation(schema, length):
    start = 0
    data_array = []
    while start < length:
        keys = schema.keys()
        row = {}
        for i in keys:
            value = ''
            if schema[i][0] == Types.BOOLEAN:
                if random.random()>0.5:
                    value = True
                else:
                    value = False
            elif schema[i][0] == Types.INT:
                value = int_gen(schema[i][2], 0)
            elif schema[i][0] == Types.VARCHAR:
                value = fake.text(max_nb_chars=schema[i][2])
            elif schema[i][0] == Types.TEXT:
                value = fake.text(max_nb_chars=schema[i][2])
            elif schema[i][0] == Types.FIRST_NAME:
                value = fake.name().split(" ")[0]
            elif schema[i][0] == Types.LAST_NAME:
                value = fake.name().split(" ")[1]
            elif schema[i][0] == Types.INT_INCREMENT:
                value = start + 1
            else:
                value = fake.date()
            row[i] = value
        data_array.append(row)
        start += 1
    print(data_array)
    
class Types(Enum):
    BOOLEAN = 1
    INT = 2
    VARCHAR = 3
    TEXT = 4
    DATE = 5
    FIRST_NAME = 6
    LAST_NAME = 7
    INT_INCREMENT = 8

sample_schema = {
    "StudentID": [Types.INT_INCREMENT, False],
    "FirstName": [Types.FIRST_NAME, False, 30],
    "LastName": [Types.LAST_NAME, False, 30],
    "DateEnrolled": [Types.DATE, False],
    "Graduated": [Types.BOOLEAN, False],
    "Bio": [Types.TEXT, False, 200],
    "Postcode": [Types.INT, False, 4]
}

sample_generation(sample_schema, 5) 
print(fake.address())

