#!/usr/bin/env python

import sys
import os
import os.path
import csv
from collections import defaultdict
import time
from datetime import datetime
#from urlparse import urlparse


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

def copy_portal_export_data(file_name):
    """copy BDO's aggregation portal export - copying each url with and without www, basically replicating the GetDomain function in Excel"""
    with open(file_name, 'rU') as file_handle:
        print file_name
        if '.txt' in file_name: 
            delim = '\t'
        else: 
            delim = ','
        reader = csv.DictReader(file_handle, delimiter=delim)
        for row in reader:           
           #need to return the equivalent of our GetDomain function in Excel
            if row['Referrer URL'][:11] == 'http://www.':
                parsed_part1 = row['Referrer URL'][11:] #get without www
                parsed_part2 = row['Referrer URL'][7:] #get with www
            elif row['Referrer URL'][:12] == 'https://www.':
                parsed_part1 = row['Referrer URL'][12:] #get without www
                parsed_part2 = row['Referrer URL'][8:] #get with www
            elif row['Referrer URL'][:8] == 'https://':
                parsed_part1 = row['Referrer URL'][8:]
                parsed_part2 = "www." + row['Referrer URL'][8:]
            else: # http://
                parsed_part1 = row['Referrer URL'][7:]
                parsed_part2 = "www." + row['Referrer URL'][7:]
            
            AD_list.append(parsed_part1)
            AD_list.append(parsed_part2)

def add_apost(string):
    """add apostrophe to any string, mainly for conserving integers when opening by double clicking in Excel"""
    return str("'" + string)

def copy_bdo_data(file_name):
    """copy file contents to a list of tuples"""
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
            
            a_tuple = (add_apost(row['ID']), ref_url, add_apost(row['Other2']), add_apost(row['IP']), add_apost(row['Date/Time']), row['Pixel Page'], file_name) #put file name here for testing
            a_list.append(a_tuple)

def copy_results_2csv(a_list, results_directory, results_file_name):
    """copy the results to a csv file"""
    complete_file_name = os.path.join(results_directory, results_file_name)
    with open(complete_file_name, 'wb') as csv_file:
        resultswriter = csv.writer(csv_file)
        resultswriter.writerow(["ID", "refURL", "Other2", "IP", "Date/Time", "Pixel Page"])
        for row in a_list:
            if row[1] in AD_list:
                resultswriter.writerow([str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5])])

#############################################################################################################################################################
#############################################################################################################################################################

if __name__ == "__main__":
    bdo_user_input_file_location = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'files_to_generate_refURL_report')
    bdo_user_input_file = os.path.join(bdo_user_input_file_location, 'BDO user input file.txt')
    pixel_directories_list = []
    pixel_directory_full_line = []
    date_list = []
    AD_list = []

    for item in os.listdir(bdo_user_input_file_location):
        count = 0
        item_path = os.path.join(bdo_user_input_file_location, item)
        if 'AD_BDO_' in item and os.path.isfile(item_path):
            count += 1
            if count > 1:
                print "\n  - There is more than 1 portal export in 'Files to generate refURL report' folder. Please make sure only 1 is in the folder and start again.\n Goodbye"
                raise SystemExit
            else:
                copy_portal_export_data(os.path.join(bdo_user_input_file_location, item)) #This is where the AD portal export data is copied
        #load user input info
        else:
            if item_path == bdo_user_input_file:
                if os.path.isfile(bdo_user_input_file):
                    with open (bdo_user_input_file, 'rb') as user_file:
                        for line in user_file:
                            if "= @" in line:
                                pixel_directories_list.append(line) #kept this a list in case more clients are added
                            if "_date =" in line:
                                date_list.append(str(line[(get_char_position(line, '=') +2):(len(line) -2)]))

    begin_date = datetime.strptime(date_list[0], '%m/%d/%Y')
    end_date = datetime.strptime(date_list[1], '%m/%d/%Y')
    data_collect_timestamp = str(datetime.strftime(end_date, '%Y%m%d'))

    #start grabbing BDOs pixel data for the desired date range
    for pixel_client_directory in pixel_directories_list:
        pixel_directory = get_pixel_directory(pixel_client_directory)
        pixel_client = pixel_client_directory[:(get_char_position(pixel_client_directory, '=')-1)]
        a_list = [] #list (easier to get unique values)
        count = 0
        for pixel_data_file in os.listdir(pixel_directory):
            file_date = pixel_data_file[len(pixel_data_file)-14 : len(pixel_data_file)-4]
            file_timestamp = datetime.strptime(file_date, '%Y-%m-%d')
            if begin_date <= file_timestamp <= end_date:
                if pixel_client == 'BDO':
                    copy_bdo_data(os.path.join(pixel_directory, pixel_data_file))
                count += 1
                print count

    b_date = str(datetime.strftime(begin_date, '%Y-%m-%d'))
    e_date = str(datetime.strftime(end_date, '%Y-%m-%d'))
    client_note = str('refURL report %s through %s' %(str(b_date), str(e_date)))

    results_directory = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'Reports')
    results_file_name = "G%s - %s %s.csv" %(data_collect_timestamp, pixel_client, client_note)
    copy_results_2csv(a_list, results_directory, results_file_name)

#need to write many more comments!!