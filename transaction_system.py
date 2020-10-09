import os.path
from os import path
import sys
import sqlite3
from datetime import datetime

conn = sqlite3.connect('transaction.db')
c = conn.cursor()

def db_check():
    TransDB_check = path.exists("transaction.db")
    if TransDB_check == True:
        print("Existing DB detected scanning for sales table")
        c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sales' ''')
        if c.fetchone()[0] == 1:
            print("Sales table has been found!")
        else:
            print("No sales table has been found. Generating....")
            c.execute('''CREATE TABLE sales (first_name TEXT NOT NULL, last_name TEXT NOT NULL, burger TEXT NOT NULL, total_bill REAL NOT NULL, current_date DATE NOT NULL, current_time TIME NOT NULL)''')
            print("Complete!")
    else:
        print("Somehting is seriously broke, check with your app dev!")
        return False 

def new_order(first_name, last_name, burger, total_bill):
    current_date = datetime.date(datetime.now())
    current_time = datetime.time(datetime.now())

    query = "INSERT INTO sales VALUES ('" + first_name + "', '" + last_name + "', '" + burger + "', '" + total_bill + "', '" + str(current_date) + "', '" + str(current_time) + "')"
    c.execute(query)
    conn.commit()

def display_menu():
    print(30 * "-" , "MENU" , 30 * "-")
    print("(1) The Impulse Burger   Price:[$12.50]")
    print("(2) Your GF said she didn't want anything burger   Price:[$13.00]")
    print("(3) All American Burger   Price:[$9.50]")
    print("(4) Western Burger   Price:[$10.00]")
    print("(5) Breakfeast for Dinner Burger   Price:[$12.75]")
    print("(6) El Diablo Burger   Price:[$11.00]")
    print("(7) End the Day and Display Stats")
    print(67 * "-")
    
def ending_program():
    print("Bye, Bye!")
    exit

def remove_whitespaces(string): 
    return string.replace(" ", "") 

def banner():
    print(
        '''        
    ____                                   _       _       _     _______                             _   _                _____           _                 
    |  _ \                                 | |     (_)     | |   |__   __|                           | | (_)              / ____|         | |                
    | |_) |_   _ _ __ __ _  ___ _ __       | | ___  _ _ __ | |_     | |_ __ __ _ _ __  ___  __ _  ___| |_ _  ___  _ __   | (___  _   _ ___| |_ ___ _ __ ___  
    |  _ <| | | | '__/ _` |/ _ \ '__|  _   | |/ _ \| | '_ \| __|    | | '__/ _` | '_ \/ __|/ _` |/ __| __| |/ _ \| '_ \   \___ \| | | / __| __/ _ \ '_ ` _ \ 
    | |_) | |_| | | | (_| |  __/ |    | |__| | (_) | | | | | |_     | | | | (_| | | | \__ \ (_| | (__| |_| | (_) | | | |  ____) | |_| \__ \ ||  __/ | | | | |
    |____/ \__,_|_|  \__, |\___|_|     \____/ \___/|_|_| |_|\__|    |_|_|  \__,_|_| |_|___/\__,_|\___|\__|_|\___/|_| |_| |_____/ \__, |___/\__\___|_| |_| |_|
                    __/ |                                                                                                       __/ |                      
                    |___/                                                                                                       |___/                       
    '''
    )
    print("Version: 1.0a")


def main():
    banner()
    db_check()
    print("Welcome to the burger joint transactional system!")
    print("System Menu:")
    loop=True      
    while loop:
        display_menu()
        choice = int(input("Enter your choice [1-7]: "))
        
        if choice==1:     
            print("The Impulse Burger has been selected... generating order")
            burger = "impulse"
            total_bill = 12.50
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, str(total_bill))
        elif choice==2:
            print("Your GF said she didn't want anything burger  has been selected... generating order")
            burger = "GF"
            total_bill = 13.00
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, str(total_bill))
        elif choice==3:
            print("All American Burger has been selected... generating order")
            burger = "American"
            total_bill = 9.50
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, str(total_bill))
        elif choice==4:
            print("Western Burger has been selected... generating order")
            burger = "Western"
            total_bill = 10.00
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, str(total_bill))
        elif choice==5:
            print("Breakfeast for Dinner Burger has been selected... generating order")
            burger = "Breakfeast"
            total_bill = 12.75
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, str(total_bill))
        elif choice==6:
            print("El Diablo Burger has been selected... generating order")
            burger = "Diablo"
            total_bill = 11.00
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, str(total_bill))
        elif choice==7:
            print("Displaying stats and ending program")
            loop=False
            ending_program()
        else:
            print("Wrong option selection. Enter any key to try again..")

main()
conn.close()