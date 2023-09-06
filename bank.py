import sys
import random
import mysql.connector

connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'bank'
)


class Bank:
    def __init__(self):        
        self.cursor = connection.cursor(dictionary=True)
    def _landing_page(self):
        print(f"Hi There!\nWelcome to Zenith Bank Plc\nIn your best Interest.\n\nPress: ENTER Register with us, 0 to Login and 1 to exit.")
        self.response = input('')
        if self.response == '':
            self.Register()
        elif self.response == '0':
            self.Login()
        elif self.response == '1':
            print('Good Bye')
            sys.exit()
        else:
            self._landing_page()            
    def Register(self):
        self.fname = input('Enter your first name: ')
        self.lname = input('Enter your last name: ')
        self.email = input('Enter your E-Mail Address: ')
        self.addr = input('Where do you live? ')
        self.password = input('Create a Password: ')
        self.acctNum = random.randint(1, 100000000000)
        sql = 'INSERT INTO users (first_name, last_name, email, acctNum, addr, password) VALUES (%s, %s, %s, %s, %s, %s)'
        val = (self.fname, self.lname, self.email, self.acctNum, self.addr, self.password )
        self.cursor.execute(sql, val)
        connection.commit()
        print(f"\nHello {self.fname} {self.lname}. Registration successful\nYou're welcome to Zenith Bank Plc. Your account number is {self.acctNum}")
        self.Login()
    def Login(self):
        print(f"\nDear User. Kindly Login to confirm that it is you!\n")
        email = input('Enter your E-Mail: ')
        password = input('Enter your Password: ')
        sql = 'SELECT * FROM users WHERE email = %s AND password = %s'
        val = (email, password)
        self.cursor.execute(sql, val)
        global user
        user = self.cursor.fetchone()        
        if user != None:
            print(f"\nDear {user['first_name']}. You are now logged in!")
            Menu().printMenu()
        else:
            print('\nInvalid Login Credentials')
            
class Menu(Bank):
    def __init__(self):
        super().__init__()
    def printMenu(self):        
        print('''
              Select a Menu to proceed!
              Zenith Bank Plc\n
              1. Check Balance          2. Transfer
              3. Airtime                4. Deposit
              5. Buy Data               99. Exit/Logout
        ''')
        self.res = input('')
        self.processMenu()
    def processMenu(self):
        if self.res == '1':
            Balance().process()
        elif self.res == '2':
            print('2')
        elif self.res == '3':
            print('3')
        elif self.res == '4':
            print('4')
        elif self.res == '5':
            print('5')
        elif self.res == '99':
            print(f"Dear {user['first_name']}! You have logged out successfully.")
            sys.exit()
        else:
            self.printMenu()

class Balance(Menu):
    def __init__(self):        
        super().__init__()
    def process(self):
        print(f'\nYour account balance is NGN9,000.89\nPress 1. OK OR 2. CANCEL')
        response = input('')
        if response == '1':
            self.printMenu()
        elif response == '2':
            print('\nOperation cancelled.\nExit!')
            sys.exit()
        else:
            print('\nInvalid Service Code')
            sys.exit()

class Transfer(Menu):
    def __init__(self):
        super().__init__()
    def process():
        print('Me')
    
bank = Bank()
bank._landing_page()