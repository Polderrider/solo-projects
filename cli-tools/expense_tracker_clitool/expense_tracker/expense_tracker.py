""" 
started: Friday 27 March 11:30
finsihed: 
Notes:

 """

import argparse
import csv
import datetime
import os
from prettytable import from_csv



# ---- Utils ------------------------------------------------------------

def csv_io(func):
    """ decorator to read/write list/csv  """
    def wrapper(*args, **kwargs):

        if not os.path.exists("data/transactions.csv"):     
            print("check")
            rows = []
            # print("does not exist")
        else:
            # open file
            with open("data/transactions.csv", "r") as f:
                reader = csv.DictReader(f)          # reader is type <class csv.DictReader> which is not iterable. convert to list
                rows = [row for row in reader]      # or rows = list(reader)

            # call function
            amended_rows, updated = func(rows, *args, **kwargs)          # rows is type list, which is iterable
            
            # write data
            fieldnames = ["id", "date", "description", "amount"]
            with open("data/transactions.csv", "w", newline="") as output:      #TODO tracker setup = no file: when data folder empty, user inputs filename
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(amended_rows)   # .writerow() has in built iteration to loop over iterables
                # print("completed")
            return updated
          
    return wrapper

def get_id(rows): 

    if len(rows) == 0:
        id = 1
    else:
       last = rows[-1]["id"]
       id = int(last) + 1
    return id

def get_date():
    # SNIPPET datetime - YYYY-MM-DD
    return datetime.datetime.today().strftime('%Y-%m-%d')

def currency(value):
    # 0 1 2 3 4 5 6
    # 1 0
    # 1 0 0
    # 1 , 0 0 0
    # 1 0 , 0 0 0
    # 1 0 0 , 0 0 0

    

    return f"${value}"


# ---- Business logic ------------------------------------------------------------

@csv_io
def add_expense(rows, args):

    if args.amount <= 0:
        print("Amount must be [bold green]greater[/bold green] than 0.")
        return

    updated = 0

    record = {
        "id": get_id(rows), 
        "date":get_date(), 
        "description": args.description, 
        "amount": (args.amount)
        }
    updated += 1
    
    rows.append(record)
    
    print(f"Expense added successfully (ID: {record["id"]})")
    return rows, updated

@csv_io
def update_expense(rows, args):
    updated = 0

    # amend row data
    for row in rows:
        if row["id"] == args.id:
            
            row["description"] = args.description
            row["amount"] = args.amount
            updated += 1

    return rows, updated    # updated is type int

@csv_io
def delete_expense(rows, args):
    new = []
    # delete row with matching id
    for row in rows:
        if row["id"] != args.id:
            new.append(row)

    removed = len(rows) - len(new)
    print("Expense deleted successfully")

    return new, removed 


def display(args):
    # TODO display transactions by user selected month
        
    # input type list of dict
    with open("data/transactions.csv") as fp:
        mytable = from_csv(fp)
        mytable.custom_format["amount"] = lambda f, v: currency(v)
        print(mytable)


def get_total(args):
    # TODO add decorator @csv_io

    months = "January February March April May June July August September October November December"
    month_names = months.split(" ")

    total = 0
    number = args.month
    with open("data/transactions.csv", "r") as f:
        transactions = csv.DictReader(f)
        for record in transactions: 

            # sum month selected only
            year, month, day = record["date"].split("-")
            if args.month and int(month) == args.month:
                total += int(record["amount"])

            # sum all records
            elif not args.month:
                total += int(record["amount"])

                
    if args.month:
        print(f"Total expenses for {month_names[number-1]}: {currency(total)}")
    else:
        print(f"Total expenses: {currency(total)}")



# ---- Entry Point ------------------------------------------------------------

def main():

    # TODO add details to parser help menu
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Expense Tracker Commands")

    # add new expense
    add = subparsers.add_parser("add")
    add.add_argument("--description", type=str)
    add.add_argument("--amount", type=int)
    add.set_defaults(func=add_expense)

    # delete expense
    delete = subparsers.add_parser("delete")
    delete.add_argument("--id", type=str)
    delete.set_defaults(func=delete_expense)

    # update expense
    update = subparsers.add_parser("update")
    update.add_argument("--id", type=str)
    update.add_argument("--description", type=str)
    update.add_argument("--amount", type=int)
    update.set_defaults(func=update_expense)


    # list all expenses
    transactions = subparsers.add_parser("transactions")
    transactions.add_argument("--month", type=int)
    transactions.set_defaults(func=display)

    # sum expenses; by month
    total = subparsers.add_parser("summary")
    total.add_argument("--month", type=int)
    total.set_defaults(func=get_total)


    # collect args provided at cmd line and allocate to result
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
    
    



