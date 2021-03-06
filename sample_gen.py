"""
Created on Sat Apr 30 10:12:04 2022

@author: daniel
"""

from generator.classes import Actions, Types, Magic
from generator.main import generate_sample_data
from attribute_maker.classes import Attribute
from attribute_maker.main import create_attributes
from example import main

''' Function to run the program (2 Options for the action) '''
def run(action, 
        table_name, 
        schema={"Year": Attribute(Types.WILDCARD, False, None, [2022])}, 
        limit=1, 
        apply_process=False, 
        magic=Magic.DEFAULT):
    if action == Actions.GET_ATTRIBUTES:
        create_attributes(table_name)
    elif action == Actions.GENERATE_SAMPLE_DATA:
        generate_sample_data(table_name, schema, limit, apply_process, magic)

# Example query
run(Actions.GENERATE_SAMPLE_DATA, "TEAM_MEMBER", main.TEAM_MEMBER, 100, True, Magic.PROCESS_TEAM_MEMBERS)
