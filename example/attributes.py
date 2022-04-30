# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 10:07:18 2022

@author: daniel
"""

from attribute_maker.attribute_maker import Attribute
from generator.generator import Types, Magic


       
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

# Race
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


