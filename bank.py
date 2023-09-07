import sys
import random
import mysql.connector as server

conn = server.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'bank'
)


class Bank:
    def __init__(self):        
        self.cursor = conn.cursor(dictionary=True)
    def _landing_page(self):
        print(f"Hi There!\nWelcome to Zenith Bank Plc\nIn your best Interest.\n\nPress: ENTER Register with us, 0 to Login and 1 to exit.")
        self.response = input('\n')
        if self.response == '':
            self.Register()
        elif self.response == '0':
            self.Login()
        elif self.response == '1':
            print('\nGood Bye!')
            sys.exit()
        else:
            self._landing_page()            
    def Register(self):
        self.fname = input('Enter your first name: ')
        self.lname = input('Enter your last name: ')
        self.email = input('Enter your E-Mail Address: ')
        self.addr = input('Where do you live? ')
        self.phoneNum = input('Phone Number: ')
        self.password = input('Create a Password: ')
        self.acctNum = random.randint(1000000000, 2000000000)
        sql = 'INSERT INTO users (first_name, last_name, email, acctNum, addr, phoneNum, password) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        val = (self.fname, self.lname, self.email, self.acctNum, self.addr, self.phoneNum, self.password )
        self.cursor.execute(sql, val)
        conn.commit()
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
            5. Change PIN             99. Exit/Logout
        ''')
        self.res = input('\n')
        self.processMenu()
    def processMenu(self):
        if self.res == '1':
            Balance().process()
        elif self.res == '2':
            Transfer().process()
        elif self.res == '3':
            Airtime().process()
        elif self.res == '4':
            Deposit().process()
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
        sql = f"SELECT acctBal FROM users WHERE user_id = {user['user_id']}"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        print(f"\nYour account balance is NGN{result['acctBal']}\nPress 1. MAIN MENU OR 2. CANCEL")
        response = input('\n')
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
    def process(self):
        amount = int(input('Enter Amount: '))
        acctNum = input('Recipient Account Number: ')
        sql = 'SELECT first_name, last_name, acctBal FROM users where acctNum = %s'
        self.cursor.execute(sql, [ acctNum ])
        userDetails = self.cursor.fetchone()
        if userDetails != None:
            print(f"\nTransfer NGN{float(amount)} to {userDetails['first_name']} {userDetails['last_name']}?\nPRESS 1 to Continue OR 2 to Cancel")
            res = input('')
            if res == '1':
                if float(amount) <= float(user['acctBal']):                    
                    sql = 'UPDATE users SET acctBal = %s WHERE acctNum = %s'
                    val = [(float(userDetails['acctBal']) + float(amount), acctNum), (float(user['acctBal']) - float(amount), user['acctNum'])]
                    for each in val:
                        self.cursor.execute(sql, each)
                    conn.commit()
                    print(f"\nYou have successfully transferred {float(amount)} to {userDetails['first_name']} {userDetails['last_name']}\nPRESS 1 for MENU or 2 to EXIT")
                    res = input('')
                    if res == '1':
                        self.printMenu()
                    elif res == '2':
                        sys.exit()
                    else: 
                        print('\nInvalid Service Code')
                        sys.exit()
                else:
                    print('Insufficient Balance')
            elif res == '2':
                self.printMenu()
            else:
                print('\nInvalid Service Code')
                sys.exit()
        else:
            print('\nAccount Number does not exist')
            self.printMenu()

class Deposit(Menu):
    def __init__(self):
        super().__init__()
    def process(self):
        amount = input('\nDeposit Amount: ')
        sql = 'SELECT acctBal FROM users WHERE user_id = %s'
        self.cursor.execute(sql, [ user['user_id'] ])
        result = self.cursor.fetchone()
        print(f"\nDear {user['first_name']}!\nAre you sure you want to deposit NGN{float(amount)} into your account?\n1. YES  2. NO")
        res = input('\n')
        if res == '1':
            sql = 'UPDATE users SET acctBal = %s WHERE user_id = %s'
            val = (float(amount) + float(result['acctBal']), user['user_id'])
            self.cursor.execute(sql, val)
            conn.commit()
            print(f"\nDeposit of NGN{float(amount)} was successful!\nPRESS 1 to go to Main Menu\n")
            res = input('')
            if res == '1':
                self.printMenu()
            else:
                sys.exit()
        elif res == '2':
            print('\nOperation Cancelled!\nPRESS 1 to go to Main Menu\n')
            res = input('')
            if res == '1':
                self.printMenu()
            else:
                sys.exit()            
        else:
            print('Invalid Service Code\n\n')

class Airtime(Menu):
    def __init__(self):
        super().__init__()
    def process(self):
        print('\nPRESS 1. Self  2. Others')
        response = input('\n')
        amount = input('\nEnter Amount: ')
        if response == '1':
            sql = f"SELECT acctBal FROM users WHERE user_id = {user['user_id']}"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if float(result['acctBal']) >= float(amount):
                sql = f"UPDATE users SET acctBal = {float(result['acctBal']) - float(amount)}"
                self.cursor.execute(sql)
                conn.commit()
                print(f"\nRecharge Card of NGN{amount} was successful.\nPRESS 1 to go to MAIN MENU or any other to key to EXIT")
                res = input('\n')
                if res == '1':
                    self.printMenu()
                else:
                    sys.exit()
            else:
                print('\nInsufficient Balance')
                sys.exit()
        elif response == '2':
            phone = input('\nRecipient Phone Number: ')
            sql = f"SELECT acctBal FROM users WHERE user_id = {user['user_id']}"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if float(result['acctBal']) >= float(amount):
                sql = f"UPDATE users SET acctBal = {float(result['acctBal']) - float(amount)}"
                self.cursor.execute(sql)
                conn.commit()
                print(f"\nRecharge Card of NGN{amount} has been sent to {phone}.\nPRESS 1 to go to MAIN MENU or any other to key to EXIT")
                res = input('\n')
                if res == '1':
                    self.printMenu()
                else:
                    sys.exit()
            else:
                print('\nInsufficient Balance')
                sys.exit()
        else:
            sys.exit

    
bank = Bank()
bank._landing_page()