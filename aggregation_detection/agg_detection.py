#!/usr/bin/env python

import os
import os.path
import csv
from collections import defaultdict
import time
from datetime import datetime


def get_pixel_directory(input_text,):
    """get pixel directory from the file uploaded by the user"""
    for index, character in enumerate(input_text):
        if character == "@":
            char_location = int(index) + 1
    pixel_directory = input_text[char_location:(len(input_text)-2)]
    return pixel_directory

def get_char_position(input_text, char):
    """get the position of the character entered"""
    for index, character in enumerate(input_text):
        if character == char:
            char_location = int(index) #+ 1
    return char_location

def copy_file_data(file_name):
    """copy file contents to dictionaries"""
    with open(file_name, 'rU') as file_handle:
        print file_name
        if '.txt' in file_name: 
            delim = '\t'
        else: 
            delim = ','
        reader = csv.DictReader(file_handle, delimiter=delim)
        for row in reader:
            a_tuple = ()
            a_tuple = (row['Referring URL'], str("'" + row['ID']), file_name) #play with this
            a_list2.append(a_tuple)

def copy_bdo_data(file_name):
    """copy file contents to dictionaries"""
    with open(file_name, 'rU') as file_handle:
        print file_name
        if '.txt' in file_name: 
            delim = '\t'
        else: 
            delim = ','
        reader = csv.DictReader(file_handle, delimiter=delim)
        for row in reader:
            a_tuple = ()
            if row['Other1'] != '':
                ref_url = row['Other1']
            else:
                ref_url = row['Referring URL']
            a_tuple = (ref_url, str("'" + row['ID']), file_name) #play with this

            a_list2.append(a_tuple)

# Load user_input audit information into a list
user_input_information_file = "Pixel Data Directories.txt"
pixel_directories_list = []
pixel_directory_full_line = []
date_list = []
os.chdir('C:\\Users\\ralbright\\Desktop\py\\aggregation_detection')
if os.path.isfile(user_input_information_file):
    with open (user_input_information_file, 'rb') as user_file:
        for line in user_file:
            if "= @" in line:
                pixel_directories_list.append(line)
            if "_date =" in line:
                date_list.append(str(line[(get_char_position(line, '=') +2):(len(line) -2)]))
else:
    print "\n  - I can't find the 'Pixel Data Directories.txt' file. Please locate the file and put it in the same folder as this aggregation detection python file is located.\n Goodbye"
    raise SystemExit 

begin_date = datetime.strptime(date_list[0], '%m/%d/%Y')
end_date = datetime.strptime(date_list[1], '%m/%d/%Y')
data_collect_timestamp = str(datetime.strftime(end_date, '%Y-%m'))

#start working with each client
for pixel_client_directory in pixel_directories_list:
    pixel_directory = get_pixel_directory(pixel_client_directory)
    pixel_client = pixel_client_directory[:(get_char_position(pixel_client_directory, '=')-1)]
    if pixel_client == 'BDO':
        BDO = True
        client_note = 'AD Pixel Data - pre UrlVN deduping'
    else:
        BDO = False
        client_note = 'AD Pixel Data'
    os.chdir(pixel_directory)
    a_list2 = [] #list of tuples (easier to get unique values)
    count = 0
    for pixel_data_file in os.listdir(pixel_directory):
        file_date = pixel_data_file[len(pixel_data_file)-14 : len(pixel_data_file)-4]
        file_timestamp = datetime.strptime(file_date, '%Y-%m-%d')
        if begin_date <= file_timestamp <= end_date:
            #if 'bdo_export' in pixel_data_file:
            if BDO == True:
                copy_bdo_data(pixel_data_file)
            else:
                copy_file_data(pixel_data_file)
            count += 1
            print count
    seen = set()
    a_list2_unique = [item for item in a_list2 if item[0] not in seen and not seen.add(item[0])]
    os.chdir("C:\\Users\\ralbright\\Desktop\\py\\aggregation_detection\\test_results")
    with open("%s - %s %s.csv" %(data_collect_timestamp, pixel_client, client_note), 'wb') as csv_file:
        resultswriter = csv.writer(csv_file)
        resultswriter.writerow(["ID", "URL"])
        for i, tup in enumerate(a_list2_unique):
            resultswriter.writerow([str(a_list2_unique[i][1]), str(a_list2_unique[i][0])])

os.chdir("C:\\Users\\ralbright\\Desktop\\py\\aggregation_detection")


# Notes -
# 1). DONE - put non-unique data in another file to be able to verify results EDIT: this is easier with just looping through list, plus too much data to put on one xlsx file
# 2). DONE - (see#1) in this same file, print the variables, like dates and file paths, etc (for testing purposes)
# 3). Need to update to dedupe on unique URL and MID combination (explains why we didn't get same results in the past)
# 4). Investigate where 'None' is coming from (it's not in the macro version of results)
# 5). DONE - (I think this is ok) Play with including file name to find why the parsing is effed up
# 6). don't collect blanks or None