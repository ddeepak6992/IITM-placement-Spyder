# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 00:27:31 2015

@author: deep
"""

#####################################
USERNAME = ''						
PASSWORD = ''
#####################################

import json
from scraper import scraper
import os
import time

def diff(A,B):
    if len(A.keys()) > len(B.keys()):
        A,B = B,A
    for k in A.keys():
        if A[k]!=B[k]:
            print '--',k,A[k]
            print '++',k,B[k]
            print ''

while True:
    try:
        if os.path.exists(os.path.join(os.getcwd(),'database.json')):    
            with open('database.json','r') as fin:
                old_database = json.load(fin)
            new_database = scraper(USERNAME, PASSWORD)
            if new_database != old_database:
                diff(old_database, new_database)
                with open('database.json', 'w') as fout:
                    json.dump(new_database, fout)
        else:
            new_database = scraper(USERNAME, PASSWORD)
            with open('database.json', 'w') as fout:
                json.dump(new_database, fout)
        time.sleep(60*60)
    except Exception as e:
        print e
