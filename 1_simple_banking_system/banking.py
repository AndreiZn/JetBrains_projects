# Write your code here
from random import randint
import sqlite3

class User:
    # the constructor
    def __init__(self, number = None, pin = None, balance = 0):
        self.account_id = None
        self.card_number = number
        self.pin = pin
        self.balance = balance
    
    # generate card number 40000***...*
    def generate_card_number(self):
        self.card_number = '400000'
        self.account_id = ''
        for i in range(9):
            self.account_id += str(randint(0,9))
        self.card_number += self.account_id
        self.check_sum()
        return self.card_number
    
    # check card number with a Luhn algorithm
    def check_sum(self):
        luhn_sum = Luhn_alg(self.card_number)
        last_digit = 10 - luhn_sum
        last_digit = last_digit % 10
        self.card_number += str(last_digit)
        
    # generate pin from 0000 to 9999
    def generate_pin(self):
        self.pin = ""
        for i in range(4):
            num = randint(0, 9)
            if num == 0:
                self.pin += "0"
            else:
                self.pin += str(num)
        return self.pin

def Luhn_alg(card_num):
    cnum = list(card_num)
    for i in range(0, len(cnum), 2):
        digit = int(cnum[i])
        digit *= 2
        if digit > 9:
            digit -= 9
        cnum[i] = str(digit)
    Luhn_sum = sum([int(cnum[i]) for i in range(len(cnum))])

    return Luhn_sum % 10



def print_menu(fl):
    if fl:
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
    else:
        print('1. Balance')
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')

def update_balance(cur, conn, us):
    cur.execute('DELETE FROM card WHERE number = ' + us.card_number)
    conn.commit()
    cur.execute('INSERT INTO card (number, pin, balance) VALUES (' + us.card_number + ', ' + us.pin + ', ' + str(us.balance) + ');')
    conn.commit()

# flag: 1 if the program should keep running; 0 otherwise (if the user pressed Exit)
program_work_flag = 1
# flag: 1 if account has to be created; 0 otherwise
account_flag = 1
# list of users
users = []

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
conn.commit()
# # if 'card.s3db' not in os.listdir('./'):
#
#
while program_work_flag:
    print_menu(account_flag)
    # user input
    ui = int(input('>'))
    print('')
    if ui == 0:
        program_work_flag = 0
        print('Bye!')
        break

    if account_flag == 1:
        if ui == 1:
            user = User()
            # users.append(user)
            card_number = user.generate_card_number()
            pin = user.generate_pin()
            cur.execute('INSERT INTO card (number, pin) VALUES (' + user.card_number + ', ' + user.pin + ');')
            conn.commit()
            print('Your card has been created')
            print('Your card number:')
            print(card_number)
            print('Your card PIN:')
            print(pin)
            print('')
        elif ui == 2:
            cur.execute('SELECT id, number, pin, balance FROM card')
            users_tuple = cur.fetchall()
            print('Enter your card number:')
            ent_cnum = input('>')
            print('Enter your PIN:')
            ent_pin = input('>')
            print('')

            u_found = 0
            for u in users_tuple:
                cur_id, cur_number, cur_pin, cur_balance = u
                cur_user = User(cur_number, cur_pin, cur_balance)
                if cur_user.card_number == ent_cnum and cur_user.pin == ent_pin:
                    u_found = 1
                    sel_user = cur_user
            if u_found:
                print('You have successfully logged in!\n')
                account_flag = 0
            else:
                print('Wrong card number or PIN!\n')
    else:
        if ui == 1:
            print('Balance: ', sel_user.balance, '\n')
        elif ui == 2:
            print('Enter income:')
            income = int(input('>'))
            sel_user.balance += income
            update_balance(cur, conn, sel_user)
            print('Income was added!\n')

        elif ui == 3:
            print('Transfer')
            print('Enter card number:')
            entered_cnum = input('>')
            luhn_sum = Luhn_alg(entered_cnum)
            if luhn_sum != 0:
                print('Probably you made a mistake in the card number. Please try again!\n')
            else:
                cur.execute('SELECT id, number, pin, balance FROM card')
                users_tuple = cur.fetchall()
                u_found = 0
                for u in users_tuple:
                    cur_id, cur_number, cur_pin, cur_balance = u
                    cur_user = User(cur_number, cur_pin, cur_balance)
                    if cur_user.card_number == entered_cnum:
                        u_found = 1
                        transfer_user = cur_user
                if not u_found:
                    print('Such a card does not exist.\n')
                elif transfer_user.card_number == sel_user.card_number:
                    print("You can't transfer money to the same account!\n")
                else:
                    print('Enter how much money you want to transfer:')
                    transfer_money = int(input('>'))
                    if transfer_money > sel_user.balance:
                        print('Not enough money!\n')
                    else:
                        sel_user.balance -= transfer_money
                        transfer_user.balance += transfer_money
                        update_balance(cur, conn, sel_user)
                        update_balance(cur, conn, transfer_user)
                        print('Success!')
                        print('')
        elif ui == 4:
            cur.execute('DELETE FROM card WHERE number = ' + sel_user.card_number)
            conn.commit()
            print('The account has been closed!')
            print('')
        elif ui == 5:
            print('You have successfully logged out!\n')
            account_flag = 1


cur.close()
conn.close()
