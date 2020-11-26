from os import path
import sys
import sqlite3
import datetime
import collections


# Initial DB creation note: Won't overwrite an existing db of the same name
conn = sqlite3.connect("transaction.db")
c = conn.cursor()


def main():
    banner()
    db_check()
    while True:
        if client_limit():
            break
        else:
            pass

        '''
        if time_limit():
            ending_program()
            break
        else:
            pass
        '''

        print("System Menu:")
        display_menu()
        choice = input("Enter your choice [1-7]: ")

        if choice == "1":
            print("The Impulse Burger has been selected... generating order")
            burger = "impulse"
            total_bill = 12.50
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, total_bill)
        elif choice == "2":
            print(
                "Your GF said she didn't want anything burger  has been selected... generating order"
            )
            burger = "GF"
            total_bill = 13.00
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, total_bill)
        elif choice == "3":
            print("All American Burger has been selected... generating order")
            burger = "American"
            total_bill = 9.50
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, total_bill)
        elif choice == "4":
            print("Western Burger has been selected... generating order")
            burger = "Western"
            total_bill = 10.00
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, total_bill)
        elif choice == "5":
            print("Breakfeast for Dinner Burger has been selected... generating order")
            burger = "Breakfeast"
            total_bill = 12.75
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, total_bill)
        elif choice == "6":
            print("El Diablo Burger has been selected... generating order")
            burger = "Diablo"
            total_bill = 11.00
            first_name = input("Enter the customers first name: ")
            first_name = remove_whitespaces(first_name)
            last_name = input("Enter the customers last name: ")
            last_name = remove_whitespaces(last_name)
            new_order(first_name, last_name, burger, total_bill)
        elif choice == "7":
            print("Displaying stats and ending program")
            ending_program()
            break
        else:
            print("Wrong option selection. Enter any key to try again..")


# DB Self Check
def db_check():
    TransDB_check = path.exists("transaction.db")
    if TransDB_check == True:
        print("Existing DB detected scanning for sales table")
        c.execute(
            """SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sales' """
        )
        if c.fetchone()[0] == 1:
            print("Sales table has been found!")
            print("All systems  [OK]")
        else:
            print("No sales table has been found. Generating....")
            c.execute(
                """CREATE TABLE sales (first_name TEXT NOT NULL, last_name TEXT NOT NULL, burger TEXT NOT NULL, total_bill DECIMAL NOT NULL, order_stamp DATE DEFAULT (datetime('now','localtime')))"""
            )
            print("Complete!")
    else:
        print("Somehting is seriously broke, check with your app dev!")
        exit("Critical Error in DB detection or generation...")


# Utility functions, used for simplifying code
def remove_whitespaces(string):
    result = string.replace(" ", "")
    return result


def name_reconstruction(first_name, last_name):
    result = first_name.capitalize() + " " + last_name.capitalize()
    return result


# END

# Order creation function
def new_order(first_name, last_name, burger, total_bill):
    query = "INSERT INTO sales (first_name, last_name, burger, total_bill) VALUES (?, ?, ?, ?);"

    order_data = (first_name, last_name, burger, total_bill)
    c.execute(query, order_data)
    conn.commit()
# END

# Order Retrival Function


def select_todays_orders(column):
    current_date = datetime.datetime.now().date()
    current_date_plus1 = datetime.date.today() + datetime.timedelta(days=1)
    unmodified_query = "SELECT %s FROM sales WHERE order_stamp >= ? AND order_stamp < ?"

    modified_query = (unmodified_query % column)

    data_fill = (current_date, current_date_plus1)
    c.execute(modified_query, data_fill)
    results = c.fetchall()
    return results

# END

# Ending Functions


def client30():
    print("\n####30th client of the day####")
    results = select_todays_orders("first_name, last_name")

    try:
        client = results[29]
    except (IndexError):
        print("There is no client 30.")
    else:
        print(
            "The 30th client of the day is: ", name_reconstruction(
                client[0], client[1])
        )


def longest_name():
    print("\n####Client with the longest name####")

    results = select_todays_orders("first_name, last_name")

    try:
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
    except:
        print("There have been no sales today!")


def top_burgers():
    print("\n####Top three burgers####")
    results = select_todays_orders("burger")

    count = 0
    burger_list = []
    for item in results:
        burger_list.append(item[count])

    bugrer_tally = collections.Counter(burger_list)
    best_burger = bugrer_tally.most_common(3)

    while True:
        try:
            print('#1 Burger: ', str(best_burger[0][0]))
        except:
            print("There have been no sales today")
            break

        try:
            print('#2 Burger: ', str(best_burger[1][0]))
        except:
            print("Sorry there is only one burger type that was sold today.")
            break

        try:
            print('#3 Burger: ', str(best_burger[2][0]))
        except:
            print("Sorry there are only two burger types that were sold.")
            break
        break


def top_clients():
    print('\n####Top three best clients####')
    results = select_todays_orders("first_name, last_name, total_bill")

    if len(results) == 0:
        print("There have been no sales today!")

    list_rebuild = []
    for tuples in results:
        processed_name = name_reconstruction(tuples[0], tuples[1])
        list_rebuild.append((processed_name, tuples[2]))

    client_total = {}

    for record in list_rebuild:
        if record[0] in client_total:
            entry_value = client_total[record[0]]
            updated_value = entry_value + record[1]
            client_total[record[0]] = updated_value
        else:
            client_total[record[0]] = record[1]

    sort_clients = sorted(client_total.items(),
                          key=lambda x: x[1], reverse=True)
    try:
        print(list(sort_clients)[0][0] + ": " + str(list(sort_clients)[0][1]))
    except:
        print("There have been no sales today!")
    try:
        print(list(sort_clients)[1][0] + ": " + str(list(sort_clients)[1][1]))
    except:
        print("Only one client today!")
    try:
        print(list(sort_clients)[2][0] + ": " + str(list(sort_clients)[2][1]))
    except:
        print("Only two clients today!")
    
    
def second_lowest_sale():
    print('\n####Second Lowest Sale####')
    results = select_todays_orders("first_name, last_name, total_bill")

    if len(results) == 0:
        print("There have been no sales today!")

    list_rebuild = []
    for tuples in results:
        processed_name = name_reconstruction(tuples[0], tuples[1])
        list_rebuild.append((processed_name, tuples[2]))

    client_total = {}

    for record in list_rebuild:
        if record[0] in client_total:
            entry_value = client_total[record[0]]
            updated_value = entry_value + record[1]
            client_total[record[0]] = updated_value
        else:
            client_total[record[0]] = record[1]

    sort_clients = sorted(client_total.items(),
                          key=lambda x: x[1], reverse=False)

    print("Name and total of second lowest sale: ",
          sort_clients[1][0], sort_clients[1][1])


def todays_total_sales():
    print('\n####Todays total sales####')
    results = select_todays_orders("total_bill")
    todays_total = 0

    sales_list = []
    for x in results:
        sales_list.append(x[0])

    for y in sales_list:
        todays_total = todays_total + y
    if todays_total > 0:
        print("Todays total earnings: ", todays_total)
    else:
        print("There have been no sales today!")


def best_hour_sales():
    print('\n####Best hour for sales####')
    results = select_todays_orders("order_stamp, total_bill")

    processed_values = {}
    for record in results:
        string_to_hour = datetime.datetime.strptime(
            record[0], '%Y-%m-%d %H:%M:%S').hour

        if string_to_hour in processed_values:
            processed_values[string_to_hour] = processed_values[string_to_hour] + record[1]
        else:
            processed_values[string_to_hour] = record[1]

    sort_money = sorted(processed_values.items(),
                        key=lambda x: x[1], reverse=True)

    try:
        print("The hour of the day with the most sales is: ", str(sort_money[0][0]) + ":00")
    except:
        print("Sorry no sales for today!")


# END

# Static Limits checked at every menu cycle


def client_limit():
    results = select_todays_orders("first_name, last_name")
    clients_processed = len(results)

    if clients_processed > 100:
        print(
            "You have reached the 100 clients that are permissible, displaying stats and ending program..."
        )
        ending_program()
        return True
    else:
        print("Clients processed today: ", clients_processed)


def time_limit():
    current_time = datetime.datetime.now().time()
    start_time = datetime.time(hour=10, minute=0, second=0, microsecond=0)
    stop_time = datetime.time(hour=22, minute=0, second=0, microsecond=0)

    if current_time <= start_time or current_time >= stop_time:
        print("Time condition violated... ending program")
        return True
    else:
        print("The time is currently ", current_time)


# END

# Function should be called when gracefully terminating the program
def ending_program():
    client30()
    longest_name()
    top_burgers()
    top_clients()
    todays_total_sales()
    second_lowest_sale()
    best_hour_sales()
    print("Bye, Bye!")


# END

# Menu Functions
def banner():
    print(
        """
    ____                                   _       _       _     _______                             _   _                _____           _
    |  _ \                                 | |     (_)     | |   |__   __|                           | | (_)              / ____|         | |
    | |_) |_   _ _ __ __ _  ___ _ __       | | ___  _ _ __ | |_     | |_ __ __ _ _ __  ___  __ _  ___| |_ _  ___  _ __   | (___  _   _ ___| |_ ___ _ __ ___
    |  _ <| | | | '__/ _` |/ _ \ '__|  _   | |/ _ \| | '_ \| __|    | | '__/ _` | '_ \/ __|/ _` |/ __| __| |/ _ \| '_ \   \___ \| | | / __| __/ _ \ '_ ` _ \
    | |_) | |_| | | | (_| |  __/ |    | |__| | (_) | | | | | |_     | | | | (_| | | | \__ \ (_| | (__| |_| | (_) | | | |  ____) | |_| \__ \ ||  __/ | | | | |
    |____/ \__,_|_|  \__, |\___|_|     \____/ \___/|_|_| |_|\__|    |_|_|  \__,_|_| |_|___/\__,_|\___|\__|_|\___/|_| |_| |_____/ \__, |___/\__\___|_| |_| |_|
                    __/ |                                                                                                       __/ |
                    |___/                                                                                                       |___/
    """
    )
    print("Version: 1.0a")
    print("Welcome to the burger joint transactional system!")


def display_menu():
    print(30 * "-", "MENU", 30 * "-")
    print("(1) The Impulse Burger   Price:[$12.50]")
    print("(2) Your GF said she didn't want anything burger   Price:[$13.00]")
    print("(3) All American Burger   Price:[$9.50]")
    print("(4) Western Burger   Price:[$10.00]")
    print("(5) Breakfeast for Dinner Burger   Price:[$12.75]")
    print("(6) El Diablo Burger   Price:[$11.00]")
    print("(7) End the Day and Display Stats")
    print(67 * "-")


# END

if __name__ == "__main__":
    main()
    conn.close()
