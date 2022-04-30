# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 10:12:04 2022

@author: daniel
"""

from generator.generator import Actions, Magic, Types, generate_sample_data
from attribute_maker.attribute_maker import Attribute, create_attributes
from example.attributes import * # All attributes

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

# Example statement
run(Actions.GENERATE_SAMPLE_DATA, "TEAM_MEMBER", TEAM_MEMBER, 100, True, Magic.PROCESS_TEAM_MEMBERS)
