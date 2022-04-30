# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 10:02:59 2022

@author: danie;
"""
import math
import random
from generator.generator import Magic

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

''' Custom method for handling duplicates '''
def prevent_duplicates(index):
    if index < 500:
        return index + 1
    else:
        return random.randint(1, 500)
    

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
    #print("coach_ids = {}".format(str(coaches_list)))
    #print("medical_ids = {}".format(str(medical_list)))
    #print("swimmer_ids = {}".format(str(swimmers_list)))
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




