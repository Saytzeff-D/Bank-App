import sys
import random
import mysql.connector as server
import pwinput
import termtables as term_tb
from colorama import init, Fore

init()

print(Fore.YELLOW,'\n>>> Initialising Database Connection...')

try:
    conn = server.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'bank'
    )
except server.errors.DatabaseError:
    print(Fore.RED, '\n>>> Refused to connect...\n>>> Check your database connection')
    sys.exit()
else:
    print(Fore.GREEN,'\n>>> Connection Initialised Successfully')

class Bank:
    def __init__(self):        
        self.cursor = conn.cursor(dictionary=True)
    def _landing_page(self):
        print(f"{Fore.RESET}\nHi There!\nWelcome to Zenith Bank Plc\nIn your best Interest.\n\nPress: ENTER Register with us, 0 to Login and 1 to exit.")        
        self.response = input('\n').strip()
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
        self.fname = input('Enter your first name: ').strip()
        self.lname = input('Enter your last name: ').strip()
        self.email = input('Enter your E-Mail Address: ').strip()
        self.addr = input('Where do you live? ').strip()
        self.phoneNum = input('Phone Number: ').strip()
        self.password = pwinput.pwinput('Create a Password: ').strip()
        self.acctNum = random.randint(1000000000, 2000000000)
        sql = 'INSERT INTO users (first_name, last_name, email, acctNum, addr, phoneNum, password) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        val = (self.fname, self.lname, self.email, self.acctNum, self.addr, self.phoneNum, self.password )
        self.cursor.execute(sql, val)
        conn.commit()
        print(f"\nHello {self.fname} {self.lname}. Registration successful\nYou're welcome to Zenith Bank Plc. Your account number is {self.acctNum}")
        self.Login()
    def Login(self):
        print("\nDear User. Kindly Login to confirm that it is you!\n")
        email = input('Enter your E-Mail: ').strip()
        password = pwinput.pwinput('Enter your Password: ').strip()
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
            5. Change PIN             6. Check History
            99. Exit/Logout
        ''')
        self.res = input('\n').strip()
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
            Pin().process()
        elif self.res == '6':
            History().process()
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
        print(f"\nYour account balance is NGN{result['acctBal']}\n\nPress 1. MAIN MENU OR 2. CANCEL")
        response = input('\n').strip()
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
        amount = int(input('Enter Amount: ').strip())
        acctNum = input('Recipient Account Number: ').strip()
        sql = 'SELECT user_id, first_name, last_name, acctBal FROM users where acctNum = %s'
        self.cursor.execute(sql, [ acctNum ])
        beneficiary = self.cursor.fetchone()
        if beneficiary != None:
            print(f"\nTransfer NGN{float(amount)} to {beneficiary['first_name']} {beneficiary['last_name']}?\n\nPRESS 1 to Continue OR 2 to Cancel")
            res = input('').strip()
            if res == '1':
                pin = input('Enter Pin: ').strip()
                sql = f"SELECT pin FROM users WHERE user_id = {user['user_id']}"
                self.cursor.execute(sql)
                userPin = self.cursor.fetchone()['pin']
                if userPin == pin:
                    if float(amount) <= float(user['acctBal']):                    
                        sql = 'UPDATE users SET acctBal = %s WHERE acctNum = %s'
                        debitAmount = float(user['acctBal']) - float(amount)
                        creditAmount = float(beneficiary['acctBal']) + float(amount)
                        val = [(creditAmount, acctNum), (debitAmount, user['acctNum'])]
                        self.cursor.executemany(sql, val)
                        # for each in val:
                        conn.commit()
                        trxInsertQuery = "INSERT INTO transactions (amount, trx_ref, beneficiary, type, user_id) VALUES(%s, %s, %s, %s, %s)"
                        val = [
                            (amount, str(random.randint(200000000000000, 999900999999999)), str(acctNum), 'Debit', user['user_id']),
                            (amount, str(random.randint(200000000000000, 999900999999999)), str(acctNum), 'Credit', beneficiary['user_id'])
                        ]
                        self.cursor.executemany(trxInsertQuery, val)
                        conn.commit()
                        print(f"\nYou have successfully transferred {float(amount)} to {beneficiary['first_name']} {beneficiary['last_name']}\n\nPRESS 1 for MENU or 2 to EXIT")
                        res = input('').strip()
                        if res == '1':
                            self.printMenu()
                        elif res == '2':
                            sys.exit()
                        else: 
                            print('\nInvalid Service Code')
                            sys.exit()
                    else:
                        print('\nInsufficient Balance')
                        sys.exit()
                else:
                    print('\nIncorrect Pin')
                    sys.exit()
            elif res == '2':
                self.printMenu()
            else:
                print('\nInvalid Service Code')
                sys.exit()
        else:
            print('\nAccount Number does not exist')
            sys.exit()

class Deposit(Menu):
    def __init__(self):
        super().__init__()
    def process(self):
        amount = input('\nDeposit Amount: ').strip()
        sql = 'SELECT acctBal FROM users WHERE user_id = %s'
        self.cursor.execute(sql, [ user['user_id'] ])
        result = self.cursor.fetchone()
        print(f"\nDear {user['first_name']}!\nAre you sure you want to deposit NGN{float(amount)} into your account?\n1. YES  2. NO")
        res = input('\n').strip()
        if res == '1':
            sql = 'UPDATE users SET acctBal = %s WHERE user_id = %s'
            val = (float(amount) + float(result['acctBal']), user['user_id'])
            self.cursor.execute(sql, val)
            conn.commit()
            trxInsertQuery = "INSERT INTO transactions (amount, trx_ref, beneficiary, type, user_id) VALUES(%s, %s, %s, %s, %s)"
            val = (amount, str(random.randint(200000000000000, 999900999999999)), str(user['acctNum']), 'Credit', user['user_id'])
            self.cursor.execute(trxInsertQuery, val)
            conn.commit()
            print(f"\nDeposit of NGN{float(amount)} was successful!\n\nPRESS 1 to go to Main Menu\n")
            res = input('').strip()
            if res == '1':
                self.printMenu()
            else:
                sys.exit()
        elif res == '2':
            print(f'\nOperation Cancelled!\n\nPRESS 1 to go to {("Main Menu").upper()}\n')
            res = input('').strip()
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
        response = input('\n').strip()
        amount = input('\nEnter Amount: ').strip()
        if response == '1':
            pin = input('\nEnter Pin: ').strip()
            sql = f"SELECT pin FROM users WHERE user_id = {user['user_id']}"
            self.cursor.execute(sql)
            userPin = self.cursor.fetchone()['pin']
            if userPin == pin:
                sql = f"SELECT acctBal FROM users WHERE user_id = {user['user_id']}"
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                if float(result['acctBal']) >= float(amount):
                    sql = f"UPDATE users SET acctBal = {float(result['acctBal']) - float(amount)}"
                    self.cursor.execute(sql)
                    conn.commit()
                    trxInsertQuery = "INSERT INTO transactions (amount, trx_ref, beneficiary, type, user_id) VALUES(%s, %s, %s, %s, %s)"
                    val = (amount, str(random.randint(200000000000000, 999900999999999)), str(user['phoneNum']), 'Debit', user['user_id'])
                    self.cursor.execute(trxInsertQuery, val)
                    conn.commit()
                    print(f"\nRecharge Card of NGN{amount} was successful.\n\nPRESS 1 to go to MAIN MENU or any other to key to EXIT")
                    res = input('\n').strip()
                    if res == '1':
                        self.printMenu()
                    else:
                        sys.exit()
                else:
                    print('\nInsufficient Balance')
                    sys.exit()
            else:
                print('\nIncorrect Pin')
        elif response == '2':
            phone = input('\nRecipient Phone Number: ').strip()
            pin = input('\nEnter Pin: ').strip()
            sql = f"SELECT pin FROM users WHERE user_id = {user['user_id']}"
            self.cursor.execute(sql)
            userPin = self.cursor.fetchone()['pin']
            if userPin == pin:
                sql = f"SELECT acctBal FROM users WHERE user_id = {user['user_id']}"
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                if float(result['acctBal']) >= float(amount):
                    sql = f"UPDATE users SET acctBal = {float(result['acctBal']) - float(amount)}"
                    self.cursor.execute(sql)
                    conn.commit()
                    trxInsertQuery = "INSERT INTO transactions (amount, trx_ref, beneficiary, type, user_id) VALUES(%s, %s, %s, %s, %s)"
                    val = (amount, str(random.randint(200000000000000, 999900999999999)), str(phone), 'Debit', user['user_id'])
                    self.cursor.execute(trxInsertQuery, val)
                    conn.commit()
                    print(f"\nRecharge Card of NGN{amount} has been sent to {phone}.\n\nPRESS 1 to go to MAIN MENU or any other to key to EXIT")
                    res = input('\n').strip()
                    if res == '1':
                        self.printMenu()
                    else:
                        sys.exit()
                else:
                    print('\nInsufficient Balance')
                    sys.exit()
            else:
                print('\nIncorrect Pin')
        else:
            sys.exit()

class Pin(Menu):
    def __init__(self):
        super().__init__()
    def process(self):
        print('\nDefault PIN is 0000')
        old_pin = input('Enter Old Pin: ').strip()
        new_pin = input('\nEnter New Pin: ').strip()
        confirm_new_pin = input('Confirm New Pin: ').strip()
        sql = f"SELECT pin FROM users WHERE user_id = {user['user_id']}"
        self.cursor.execute(sql)
        pin = self.cursor.fetchone()['pin']
        if pin == old_pin:
            if new_pin == confirm_new_pin:
                sql = "UPDATE users SET pin = %s WHERE user_id = %s"
                val = (new_pin, user['user_id'])
                self.cursor.execute(sql, val)
                conn.commit()
                print('\nPin changed successfully')
            else:
                print('\nPin does not match')
        else:
            print('\nOld Pin is not correct...')

class History(Menu):
    def __init__(self):
        super().__init__()
        self.history = []
    def process(self):
        sql = f"SELECT trx_ref, amount, beneficiary, type, transact_at FROM transactions WHERE user_id = {user['user_id']}"
        self.cursor.execute(sql)
        self.history = self.cursor.fetchall()
        t_data = []
        for each in self.history:
            t_data.append(list(each.values()))        
        table = term_tb.to_string(
            t_data, 
            header=['Trx Ref', 'Amount(NGN)', 'Beneficiary', 'Transaction Type', 'Transaction Date'],
            style=term_tb.styles.ascii_thin_double,
        )        
        print(f"\n{table}\n\nPRESS 1 to go to MAIN MENU or any other to key to EXIT")
        res = input('\n').strip()
        if res == '1':
            self.printMenu()
        else:
            sys.exit()
    
bank = Bank()
bank._landing_page()