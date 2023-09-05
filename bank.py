import sys
import random

class Bank:
    def __init__(self):
        self._landing_page()    
    def _landing_page(self):
        print(f"Hi There!\nWelcome to Zenith Bank Plc\nIn your best Interest.\n\nPress: ENTER Register with us, 0 to Login and 1 to exit.\n")
        self.response = input('')
        if self.response == '':
            self.Register()
        elif self.response == '0':
            self.Login({'fname': 'Admin', 'lname': 'Zenith', 'email': 'admin@zenith.com', 'addr': 'SCICT', 'acct': '90876654363'})
        elif self.response == '1':
            print('Good Bye')
            sys.exit()
        else:
            self._landing_page()
            # print(self.response)
    def Register(self):
        self.fname = input('Enter your first name: ')
        self.lname = input('Enter your last name: ')
        self.email = input('Enter your E-Mail Address: ')
        self.addr = input('Where do you live? ')
        self.acctNum = random.randint(1, 100000000000)
        self.details = { 'fname': self.fname, 'lname': self.lname, 'email': self.email, 'addr': self.addr, 'acct': self.acctNum }
        print(f"\nHello {self.fname} {self.lname}. You're welcome to Zenith Bank Plc. Your account number is {self.acctNum}")
        self.Login(self.details)
        
    def Login(self, details):
        print(f"\nDear User. Kindly Login to confirm that it is you!\n")
        email = input('Enter your E-Mail: ')
        acct = input('Enter your Account Number: ')
        if int(acct) == details['acct'] and email == details['email']:
            print(f"Dear {details['fname']}. You are now logged in!")
        else:
            print('Invalid Login Credentials')
            
class User():
    def __init__(self):
        pass
    
    
Bank()