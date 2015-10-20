#  Copyright (c) 2015 Cutting Edge QA

import json
import gspread
import re
import os

from oauth2client.client import SignedJwtAssertionCredentials

import robot
from robot.libraries.BuiltIn import BuiltIn

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, 'version.py'))

__version__ = VERSION


class TestToolsMK:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION
    
    def __init__(self, keyJsonFile=None, id=None,worksheetName=None):
         if keyJsonFile!=None:
            json_key = json.load(open(keyJsonFile))
            scope = ['https://spreadsheets.google.com/feeds']
            credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
            gc = gspread.authorize(credentials)
            if id != None:
                sht1 = gc.open_by_key(id)
                if worksheetName != None:
                    self.WORKSHEET = sht1.worksheet(worksheetName)


    def get_spreadsheet_by_id(self, file, id):
         json_key = json.load(open(file))
         scope = ['https://spreadsheets.google.com/feeds']
         credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
         gc = gspread.authorize(credentials)
         self.SPREADSHEET = gc.open_by_key(id)
         self.WORKSHEET =  self.SPREADSHEET.sheet1
    def select_worksheet_by_name(self, worksheet_name):
         self.WORKSHEET = self.SPREADSHEET.worksheet(worksheet_name)
    def get_dictonary_logins_and_passwords(self):
         login_list = self.WORKSHEET.col_values(1)
         password_list = self.WORKSHEET.col_values(2)
         return dict(zip(self.login_list, self.password_list))

    def get_password_for_login(self,login):
        """Return password for provided login, rise error when login is missing"""
        self.dictionary = self.get_dictonary_logins_and_passwords()
        return self.dictionary[login] 
    def find_cell_using_regex(self,regex):
       """Return password for provided login, rise error when login is missing"""
       pattern = r'%s' % regex
       print pattern
       amount_re = re.compile(pattern)
       return self.WORKSHEET.find(amount_re)
    def find_all_cell_using_regex(self,regex):
       """Return password for provided login, rise error when login is missing"""
       pattern = r'%s' % regex
       print pattern
       amount_re = re.compile(pattern)
       return self.WORKSHEET.findall(amount_re)