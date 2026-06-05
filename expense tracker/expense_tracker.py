import csv
import datetime as dt
import sys
import pandas as pd
from matplotlib import pyplot as plt


def authenticate(username, password):
    with open('authenticate.csv', 'r') as auth_file:
        file_reader = csv.DictReader(auth_file)

        for line in file_reader:
            if (line['username'] == username):
                if (line['password'] == password):
                    return True
        return False


def add_user(username, password):
    with open('authenticate.csv', 'r') as auth_file:
        file_reader = csv.DictReader(auth_file)
        for line in file_reader:
            if (line['username'] == username):
                print("username not available! ")
                return -1

    with open('authenticate.csv', 'a', newline='') as auth_file:
        fnames = ['username', 'password']
        file_writer = csv.DictWriter(auth_file, fieldnames=fnames)

        new_user = {}

        new_user['username'] = username
        new_user['password'] = password

        file_writer.writerow(new_user)
    with open('{}.csv'.format(username), 'w') as new_file:
        f1names = ['Name', 'Cost', 'Category', 'Date']
        new_file_writer = csv.DictWriter(new_file, fieldnames=f1names)
        new_file_writer.writeheader()


def month_expenses(username, month):
    data = pd.read_csv('{}.csv'.format(username))

    data["Date"] = pd.to_datetime(data["Date"])

    data['Month'] = data['Date'].dt.month

    month_data = data[data['Month'] == month]
    categ_grp = month_data.groupby('Category')

    categ_cost = categ_grp['Cost'].sum()

    y = categ_cost
    x = categ_cost.index

    plt.bar(x, y)
    plt.xlabel("Category")
    plt.ylabel("Total Cost")
    plt.title(f"Expenses for Month {month}")
    plt.show()


def add_expense(username):
    with open('{}.csv'.format(username), 'a', newline='') as expense_file:
        fnames = ['Name', 'Cost', 'Category', 'Date']
        expense_write = csv.DictWriter(expense_file, fieldnames=fnames)

        expense = {}
        expense['Name'] = input("Enter name of expense: ")
        expense['Cost'] = float(input("Enter cost of expense: "))
        expense['Category'] = input("Enter category of expense: ")
        expense['Date'] = dt.datetime.today()
        expense_write.writerow(expense)


def view_expenses(username):
    with open('{}.csv'.format(username), 'r') as expense_file:
        expense_reader = csv.DictReader(expense_file)

        for line in expense_reader:
            for key, value in line.items():
                print(key + ': ', value)
            print("\n")


def total_spendings(username):
    total = 0
    with open('{}.csv'.format(username), 'r') as expense_file:
        expense_reader = csv.DictReader(expense_file)

        for line in expense_reader:
            total = total + float(line['Cost'])

        print(total)


def category_total(username):
    total = 0
    categ = input("Which category? ")

    with open('{}.csv'.format(username), 'r') as expense_file:
        expense_reader = csv.DictReader(expense_file)
        for spendings in expense_reader:
            if (spendings['Category'] == categ):
                total = total + float(spendings['Cost'])

    print("Total in Category " + ": ", categ, total)


def real_task(username):
    while True:

        print("1. Add Expense\n2. View Expenses\n3. Total Spendings\n4. Category Wise Spending\n5. Sign out\n6. Month-Wise Expenses\n7. Exit")

        try:
            task = int(input("Enter task number: "))

        except ValueError:
            print("Invalid input!")
            continue

        if (task == 1):
            add_expense(username)

        elif (task == 2):
            view_expenses(username)

        elif (task == 3):
            total_spendings(username)

        elif (task == 4):
            category_total(username)

        elif (task == 5):
            print("Signing out...")
            break
        elif (task == 6):
            print("Enter month number: ")

            try:
                month = int(input())
            except ValueError:
                print("Invalid month!")
                continue
            else:
                if (month > 12 or month < 1):
                    print("Invalid month!")
                    continue

            month_expenses(username, month)

        elif (task == 7):
            print("Exiting...")
            sys.exit()

        if (task > 6 or task < 1):
            print("invalid response! ")


def sign_in():
    while True:
        print("Choose an option")
        print("1. Sign in\n2. New User\n3. Exit")

        try:
            choice = int(input())
        except ValueError:
            print("Invalid choice!")
            continue
        else:
            if (choice > 3 or choice < 1):
                print("Invalid choice!")
                continue

        if (choice == 1):
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if (authenticate(username, password)):
                print("Welcome back!")
                real_task(username)
            else:
                print("Wrong credentials entered!")
                continue

        if (choice == 2):
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            add_user(username, password)

            if (add_user == -1):
                continue

            else:
                print("User added succesfully.\nSign in to continue!")
                continue
        if (choice == 3):
            print("Exiting...")
            sys.exit()


sign_in()
