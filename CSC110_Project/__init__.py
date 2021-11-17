"""
the first file that's called
import files and data

"""

import os
import pprint

import BankruptcyData
import MediaData
import Graphing

data_dir = os.listdir('data')
temp = []

for i in range(1, len(data_dir)):    # loop through all the files in the data directory
    file = data_dir[i]
    table = BankruptcyData.load_data(data_dir[i])
    temp.append(table)

# comment out this part if you don't want your python console to explode
pprint.pprint(temp[0])
