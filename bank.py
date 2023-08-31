import sys
import random

def _landing_page():
    print(f"Hi There!\nWelcome to Zenith Bank Plc\nIn your best Interest.\n\nPress ENTER to Register with us, 0 to Login and 1 to exit.\n")
    response = input('')
    if response == '':
        Register()
    elif response == '0':
        Login(details={'fname': 'Admin', 'lname': 'Zenith', 'email': 'admin@zenith.com', 'addr': 'SCICT', 'acct': '90876654363'})
    elif response == '1':
        print('Good Bye')
        sys.exit()
    else:
        _landing_page()

def Register():
    fname = input('Enter your first name: ')
    lname = input('Enter your last name: ')
    email = input('Enter your E-Mail Address: ')
    addr = input('Where do you live? ')
    acctNum = random.randint(1, 100000000000)
    details = { 'fname': fname, 'lname': lname, 'email': email, 'addr': addr, 'acct': acctNum }
    print(f"\nHello {fname} {lname}. You're welcome to Zenith Bank Plc. Your account number is {acctNum}")
    Login(details)
    
def Login(details):
    print(f"\nDear User. Kindly Login to confirm that it is you!")
    acct = input('Enter your Account Number: ')
    email = input('Enter your E-Mail: ')
    if acct == details['acct'] and email == details['email']:
        print(f"Dear {details['fname']}. You are now logged in!")
    else:
        print('Invalid Login Credentials')
    
_landing_page()