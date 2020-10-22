import os.path
from os import path
import sys
import sqlite3
import datetime

# Initial DB creation
conn = sqlite3.connect('transaction.db')
c = conn.cursor()

# DB Self Check
def db_check():
    TransDB_check = path.exists("transaction.db")
    if TransDB_check == True:
        print("Existing DB detected scanning for sales table")
        c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sales' ''')
        if c.fetchone()[0] == 1:
            print("Sales table has been found!")
            print("All systems  [OK]")
        else:
            print("No sales table has been found. Generating....")
            c.execute('''CREATE TABLE sales (first_name TEXT NOT NULL, last_name TEXT NOT NULL, burger TEXT NOT NULL, total_bill DECIMAL NOT NULL, order_stamp DATE DEFAULT (datetime('now','localtime')))''')
            print("Complete!")
    else:
        print("Somehting is seriously broke, check with your app dev!")
        exit("Critical Error in DB detection or generation...")

# SQL Query Functions
def new_order(first_name, last_name, burger, total_bill):
    query = "INSERT INTO sales (first_name, last_name, burger, total_bill) VALUES (?, ?, ?, ?)"

    order_data = (first_name, last_name, burger, total_bill)
    c.execute(query, order_data)
    conn.commit()

# Utility Functions
def remove_whitespaces(string): 
    result = string.replace(" ", "")
    return result

def name_reconstruction(first_name, last_name):
    result =  first_name.capitalize() + " " + last_name.capitalize()
    return result

# Front Facing Functions
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


def client30():
    print("####30th client of the day####")
    current_date = datetime.datetime.now().date()
    current_date_plus1 = datetime.date.today() + datetime.timedelta(days=1)
    query = "SELECT first_name, last_name FROM sales WHERE order_stamp >= ? AND order_stamp < ?"

    date_fill = (current_date, current_date_plus1)
    c.execute(query, date_fill)
    results = c.fetchall()
    try:
        client = results[29]
    except (IndexError):
        print("There is no client 30.")
    else:
        print("The 30th client of the day is: ", name_reconstruction(client[0], client[1]))

def longest_name():
    print("####Client with the longest name####")
    query = "SELECT first_name, last_name FROM sales"

    c.execute(query)
    results = c.fetchall()
    full_name = []
    for tuples in results:
        processed_name = name_reconstruction(tuples[0], tuples[1])
        full_name.append(processed_name)
    
    full_name.sort(key=len, reverse=True)
    longest_name_length = len(full_name[0])

    final_name_list = []
    for name in full_name:
        if longest_name_length == len(name):
            final_name_list.append(name)
        else:
            pass
    
    if len(final_name_list) > 1:
        print("There are multiple names that are the longest, here is the list: ")
        for name in final_name_list:
            print(name)
    else:
        print("There were no ties for longest name, listing only entry: ")
        print(final_name_list[0])
    

def client_limit():
    current_date = datetime.datetime.now().date()
    current_date_plus1 = datetime.date.today() + datetime.timedelta(days=1)
    query = "SELECT first_name, last_name FROM sales WHERE order_stamp >= ? AND order_stamp < ?"

    date_fill = (current_date, current_date_plus1)
    c.execute(query, date_fill)
    results = c.fetchall()
    clients_processed = len(results)

    if clients_processed > 1:
        print("You have reached the 100 clients that are permissible, displaying stats and ending program...")
        ending_program()
        return True
    else:
        print("Clients processed today: ", clients_processed)

def ending_program():
    client30()
    longest_name()
    print("Bye, Bye!")

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

if __name__ == "__main__":
    banner()
    db_check()
    print("Welcome to the burger joint transactional system!")    
    while True:
        if client_limit():
            break
        else:
            pass

        print("System Menu:") 
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
            new_order(first_name, last_name, burger, total_bill)
        elif choice==2:
            print("Your GF said she didn't want anything burger  has been selected... generating order")
            burger = "GF"
            total_bill = 13.00
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, total_bill)
        elif choice==3:
            print("All American Burger has been selected... generating order")
            burger = "American"
            total_bill = 9.50
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, total_bill)
        elif choice==4:
            print("Western Burger has been selected... generating order")
            burger = "Western"
            total_bill = 10.00
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, total_bill)
        elif choice==5:
            print("Breakfeast for Dinner Burger has been selected... generating order")
            burger = "Breakfeast"
            total_bill = 12.75
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, total_bill)
        elif choice==6:
            print("El Diablo Burger has been selected... generating order")
            burger = "Diablo"
            total_bill = 11.00
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, total_bill)
        elif choice==7:
            print("Displaying stats and ending program")
            ending_program()
            break
        else:
            print("Wrong option selection. Enter any key to try again..")



conn.close()
