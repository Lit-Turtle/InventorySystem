"""
user_comp.py

Gets user input in order to control inventory classes.
Also controls account systems, allowing users to login.

This module provides classes and functions to:
 - Create, delete, and manipulates inventory system.
 - Creates inventory reports.
 - Provides menus to control inventory.
 - Allows user to create and login to accounts to modify inventory. 
 - Session to set active account and inventories

Author: Kaipo Ojas
Date: 2026-03-20 (Ended not started)
"""
from main import MasterClass, Category, Product
import os
import time
import re
import json
import bcrypt

class Session:
    """
    Class to track uer and inventory
    """
    def __init__(self, user=None, signed_in=False):
        """
        Intialize the session class

        :param user: Username to which logged into, defaults to None
        :type user: str
        :signed_in: Checks whether signed in or not, defaults to False
        :type signed_in: boolean
        """
        self.user = user
        self.signed_in = signed_in
        self.inventories = {}
    
    def logged_out(self):
        """
        Logs out user from session
        """
        self.signed_in = False
        self.user = None
    
    def logged_in(self, user):
        """
        Logs in user.
        
        :param user: the user to which logging into
        :type user: str
        """
        self.user = user
        self.signed_in = True
    
    def get_user(self):
        """
        Gets the user to which currently logged into

        :return: the user
        :rtype: str
        """
        return self.user
    
    def set_user(self, u):
        """
        Sets the user.

        :param u: new user
        :type u: str
        """
        self.user = u

session = Session(None, None)

curr_cate = []
curr_pro = []

def clear_screen():
    """
    Clears console
    """
    os.system('cls' if os.name == 'nt' else 'clear')

#=============Basic Inventory Methods============

def create_inventory():
    """
    Gets inventory name and adds inventory object to list
    """
    clear_screen()
    invent_name = input("Inventory Name: ")
    session.inventories.setdefault(invent_name, MasterClass())

def delete_inventory(invent: session.inventories):
    """
    Asks for inventory name and deletes inventory with corresponding name

    :param invent: the active inventories dict
    :type invent: dict
    """
    clear_screen()
    invent_name = input("Inventory Name: ")
    if invent_name in session.inventories:
        del session.inventories[invent_name]

def find_category(invent: session.inventories, invent_name, cate_name):
    """
    Finds category in inventory and returns whether inventory exists

    :param invent: the active inventories dict
    :type invent: dict
    :param invent_name: Name of inventory of which to search through.
    :type invent_name: str
    :param cate_name: category name of which to look for
    :type cate_name: str
    :return: returns whether specified category was found or not
    :rtype: str
    """
    return invent[invent_name].find_category(cate_name)

def get_category(invent: session.inventories, invent_name, cate_name):
    """
    Finds category in inventory and returns Category object with corresponding name

    :param invent: the active inventories dict
    :type invent: dict
    :param invent_name: Inventory name of which to find category.
    :type invent_name: str
    :param cate_name: category name to look for
    :type cate_name: str
    :return: the Category class if found
    :rtype: Category class or str
    """
    return invent[invent_name].get_category(cate_name)

def create_category(invent: session.inventories, invent_name):
    """
    Asks for category name and creates a Category object with corresponding name

    :param invent: the active inventories dict
    :type invent: dict
    :param invent_name: name of inventory of which new category should be child of
    :type invent_name: str
    """
    clear_screen()
    cate_name = input("Category Name: ")
    invent[invent_name].create_category(cate_name)

def delete_category(invent: session.inventories, invent_name):
    """
    Asks for category name and deletes Category object with corresponding name

    :param invent: the active inventories dict
    :type invent: dict
    :param invent_name:inventory in which category to delete is located
    :type invent_name: str
    """
    clear_screen()
    cate_name = input("Category Name to Delete: ")
    invent[invent_name].remove_category(cate_name)


def delete_index(invent:session.inventories, invent_name):
    """
    Not Needed or used also method does not exist

    :param invent: the active inventories dict
    :type invent: dict
    :param invent_name: inventory name of which to read through
    :type invent_name: str
    """
    clear_screen()
    cate_name = input("Category to Delete: ")
    invent[invent_name].delete_category(cate_name)

def create_product(invent: session.inventories, invent_name, cate_name, id=None):
    """
    Creates product with given inventory name and category name

    :param invent: the active inventories dict
    :type invent: dict
    :param invent_name: name of inventory of which product should be within
    :type invent_name: str
    :param cate_name: Name of category of which product should be child of.
    :type cate_name: str
    :param id: id of which new product should be, default to None
    :type id: int
    """
    clear_screen()
    name = input("Product Name: ")
    amount = input("Supply Amount: ")
    while bool(re.search(r"\D", amount)):
        amount = input("Invalid. Enter a number for amount: ")
    amount = int(amount)

    while True:
        cost = input("Price: ")
        try:
            cost = float(cost)
            break
        except ValueError:
            print("Invalid. Enter a number for price:")

    while True:
        paid = input("Paid Per: ")
        try:
            paid = float(paid)
            break
        except ValueError:
            print("Invalid. Enter a number for cost")

    category = invent[invent_name].get_category(cate_name)
    if id == None:
        category.create_product(name, amount, cost, paid, cate_name) 
    else:
        category.create_product(name, amount, cost, paid, cate_name, None) 
    
def delete_product(invent: session.inventories, invent_name, cate_name, pro_name_id):
    """
    Deletes product in corresponding category and name or id(Can remake this with new Master get_product)

    :param invent: the active inventories dict
    :type invent: dict
    :param invent_name: the name of inventory of which product to delete is within.
    :type invent_name: str
    :param cate_name: the name of category of which product to delete is child of.
    :type cate_name: str
    :param pro_name_id: product name or id of which to delete
    :type pro_name_id: str
    """
    get_category(invent, invent_name, cate_name).remove_product(pro_name_id)

def update_products(cate_name):
    """
    Seems to grab products list from category: but not used
    
    :param cate_name: name of category to update
    :type cate_name: str
    :return: list of products
    :rtype: array
    """
    for cate in curr_cate:
        if cate.get_name() == cate_name:
            return cate.get_products()

def get_product(invent_name, cate_name, pro_name_id):
    """
    Returns Product object in correspding category and name or id

    :param invent_name: Name of inventory to which to get product from
    :type invent_name: str
    :param cate_name: name of category to which to get product from
    :type cate_name: str
    :param pro_name_id; Product name or id of which to get
    :type pro_name_id: str or int
    :return: Returns the matching product class
    :rtype: Product class or Not Found
    """
    return get_category(session.inventories, curr_cate[teste_met()].get_products(), cate_name).get_product(pro_name_id)

def purchased(invent: session.inventories, invent_name, cate_name):
    """
    Category level purchase

    :param invent: the active inventories dict
    :type invent: dict
    :param invent_name: name of inventory to which purchasing product in
    :type invent_name: str
    :param cate_name: name of category to which purchasing product in
    :type cate_name: str
    """
    user_input = ''
    while(user_input != "0"):
        while(get_category(session.inventories, invent_name, cate_name).get_product(user_input) == "Not Found" or user_input == 0): 
            user_input = input("Enter Product Name or ID. Enter 0 when complete: ")
        
        #amount
        amount = input("Enter Amount Sold: ")
        invalid = True

        while invalid:
            if bool(re.search(r"\d", amount)):
                if get_category(session.inventories, invent_name, cate_name).get_product(user_input).get_supply() >= int(amount):
                    invalid = False
                    break
            amount = input("Invalid Amount. Try Again: ")
        get_category(session.inventories, invent_name, cate_name).purchased(user_input, int(amount))
        user_input = input("Enter Product Name or ID. Enter 0 when complete: ")

def invent_purchase(invent: session.inventories, invent_name):
    """
    Procceses purchases with just inventory name
    
    :param invent: the active inventories dict
    :type invent: dict
    :param invent_name: the name of inventory in which purchase occurs
    :type invent_name: str
    """
    clear_screen()
    user_input = ''
    while(user_input != "0"):
        while(invent[invent_name].has_product(user_input) == "Not Found" and user_input != "0"): 
            user_input = input("Enter Product Name or ID. Enter 0 when complete: ")
        if user_input == "0":
            break
        while True:
            amount = input("Enter Amount Sold: ")
            try:
                amount = int(amount)
                if invent[invent_name].get_product(user_input).get_supply() >= amount:
                    break
            except ValueError:
                print("Invalid Amount. Try Again.")

        invent[invent_name].purchased(user_input, amount)
        user_input = input("Enter Product Name or ID. Enter 0 when complete: ")

#==============Text Report===============
def create_report(invent: session.inventories, invent_name):
    """
    Generates a sales report in Sales Report.txt
    
    :param invent: the active inventories dict
    :type invent: dict
    :param invent_name: inventory name of which to generate report for
    :type invent_name: str
    """
    chart = ["Line 1", "Line 2"]
    with open ("Sales Report.txt", "w") as file:
        file.write(f"\tSales Report\n")

        profit = invent[invent_name].get_profit()
        revenue = invent[invent_name].get_revenue()

        #Write Bar Chart

        #Calaculate number of time divisble by 10
        divisible = 0
        r = revenue
        p = profit
        while True:
            if r / 10 >= 1 and p / 10 >= 1:
                divisible = divisible + 1
                r = r / 10
                p = p / 10
            else:
                break

        #Assigns value as long as not 0
        if divisible == 0:
            pro = int(profit)
            rev = int(revenue)
        else:
            pro = int(profit / (10 ** divisible))
            rev = int(revenue / (10 ** divisible))

        if rev != 0 and pro != 0:
            #Checks if difference is larger than 100
            if rev / pro > 10:
                pro = 1
            elif pro / rev > 10:
                rev = 1

        for i in range(10, 0, -1):
            file.write("|")

            if pro >= i:
                file.write("\tX")
            else:
                file.write("\t")
            
            if rev >= i:
                file.write("\tX\n")
            else: 
                file.write("\n")
        file.write("_____________________\n")
        file.write("\tP\tR\n")
        file.write("\tR\tE\n")
        file.write("\tO\tV\n")
        file.write("\tF\tE\n")
        file.write("\tI\tN\n")
        file.write("\tT\tU\n")
        file.write("\t\tE\n")
        
        file.write(f'\n\nProfit: {profit}\nRevenue: {revenue}\n')


        top_pro = sorted(invent[invent_name].get_pro_sold_dict().items(), key=lambda x: x[1], reverse=True)[:5]
        top_cate = sorted(invent[invent_name].get_cate_sold_dict().items(), key=lambda x: x[1], reverse=True)[:3]

        file.write("\nTop Categories: \n")
        count = 1
        for cate, num in top_cate:
            file.write(f'{count}. {cate} - {num}\n')
            count += 1

        file.write("\nTop Products: \n")
        count = 1
        for pro, num in top_pro:
            file.write(f'{count}. {pro} - {num}\n')
            count += 1

#==============User Database===============

salt = os.urandom(16) 
db_file = "users.json"

try:
    with open(db_file, "r") as f:
        db = json.load(f)
except:
        db = {"TEST": "case"}

def save_db():
    """
    Saves database to file
    """
    with open(db_file, "w") as f:
        json.dump(db, f, indent=4)

def create_account():
    """
    Creates account and saves whatever inventory currently had made
    
    :return: returns username(user) of newly created inventory
    :rtype: str
    """
    print(db)
    while True: 
        clear_screen()
        print("Create Account")
        username = input("Username: ")
        password = input("Password: ")
        confirm_password = input("Confirm Password: ")
        

        if password == confirm_password:
            if username not in db:
                password_bytes = password.encode()
                hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
                db[username] = {
                    'hash': hashed.decode(),
                    'inventory': {}
                }
                save_db()
                print("Account Created")
                break
            else:
                print("Account Already Exists")
        else:
            print("Passwords do not match")
    return db[username]

def login():
    """
    Lets user login to account

    :return: returns user if sucessfully signed in, None if not
    :rtype: str or None
    """
    clear_screen()
    print("Login")
    username = input("Username: ")
    password = input("Password: ")
    
    if username not in db:
        print("Account not found")
        return None

    stored_hash = db[username]["hash"].encode()
    password_bytes = password.encode()

    if bcrypt.checkpw(password_bytes, stored_hash):
        print("Logged in")
        return db[username]
    else:
        print("Incorrect password")
        return None

def save_all(user, inventory):
    """
    Saves inventory to json database file
    
    :param user: current user to which to save inventory to
    :type user: str
    :param inventory: inventories dict to save into file
    :type inventory: dict
    """
    print(user)
    user["inventory"] = {}
    if isinstance(user["inventory"], list):
        user["inventory"] = {}

    for invent_name, invent_obj in inventory.items():
        user["inventory"].setdefault(invent_name, {})
        for cate_obj in invent_obj.get_categories():
            user["inventory"][invent_name].setdefault(cate_obj.get_name(), {})
            for prod_obj in cate_obj.get_products():
                user["inventory"][invent_name][cate_obj.get_name()].setdefault(prod_obj.get_name(), [prod_obj.get_price(), prod_obj.get_supply(), prod_obj.get_id()])
            user["inventory"][invent_name].setdefault("Profit", invent_obj.get_profit())
            user["inventory"][invent_name].setdefault("Revenue", invent_obj.get_revenue())
    save_db()

def view_inventory():
    """
    Shows inventory
    """
    if not user["inventory"]:
        print("Inventory Empty")
        return 
    
    print("\nInventory")
    for item in user["inventory"]:
        print(item)

def load_all(user):
    """
    Loads data from json file onto active inventories
    
    :param user: the user file to which to load.
    :type user: str
    :return: returns the new loaded inventory
    :rtype: dict
    """
    session.inventories = {}
    for invent_name, invent_inner_dict in user["inventory"].items():
        session.inventories.setdefault(invent_name, MasterClass())
        for cate_name, cate_inner_dict in invent_inner_dict.items():
            if cate_name == "Profit":
                session.inventories[invent_name].set_profit(cate_inner_dict)
            elif cate_name == "Revenue":
                session.inventories[invent_name].set_revenue(cate_inner_dict)
            else:
                session.inventories[invent_name].create_category(cate_name)
                for pro_name, pro_info in cate_inner_dict.items():
                    if len(pro_info) == 3:
                        session.inventories[invent_name].get_category(cate_name).create_product(pro_name, pro_info[1], pro_info[0], 0, cate_name, pro_info[2])
                    else:
                        session.inventories[invent_name].get_category(cate_name).create_product(pro_name, pro_info[1], pro_info[0], 0, cate_name)
    return session.inventories

#========User Menus=============

def menu_one(invent: session.inventories, session): 
    """
    Top level, Inventory level, shows all inventories.
    :param invent: the active inventories dict
    :type invent: dict
    :param session: session class to track user logins or logout
    :type session: Session class
    """
    clear_screen()
    number_name_pair = {}
    count = 1
    for x,y in session.inventories.items():
        number_name_pair.setdefault(count, x)
        print(f'{count}: {x}')
        count = count + 1
    print(f'{count}. Create Inventory')
    count = count + 1
    print(f'{count}. Delete Inventory')

    if session.signed_in:
        count = count + 1
        print(f'{count}. Logout')
    else:
        count = count + 1
        print(f'{count}. Create Account')        
        count = count + 1
        print(f'{count}. Login')

    count = count + 1
    print(f'{count}. Quit')
    

    if session.signed_in:
        create_index = count - 3
        delete_index = count - 2
        logout_index = count - 1

        create_acc_index = -10
        login_index = -10
    else:
        create_index = count - 4
        delete_index = count - 3
        create_acc_index = count - 2
        login_index = count - 1  

        logout_index = -10

    quit_index = count

    user_choice = input("Enter Corresponding Number: ")

    while (bool(re.search(r"\D", user_choice)) or user_choice == ""):
        user_choice = input("Invalid. Enter Corresponding Number: ")
    
    user_choice = int(user_choice)

    match(user_choice):
        case _ if user_choice == quit_index:
            return
        case _ if user_choice == logout_index:
            session.logged_out()
            session.inventories = {} #  
            menu_one(session.inventories, session)
            return
        case _ if user_choice == create_acc_index:
            user = create_account()
            session.set_user(user)
            save_all(session.get_user(), session.inventories)
            menu_one(session.inventories, session)
            return
        case _ if user_choice == login_index:
            user = login()

            if user is not None:
                session.logged_in(user)
                session.inventories = load_all(user) #
            else:
                print("Login Failed")
                time.sleep(2)

            menu_one(session.inventories, session)
            return
        case _ if user_choice == delete_index:
            if session.inventories:
                delete_inventory(session.inventories)
                if session.signed_in:
                    save_all(session.get_user(), session.inventories)
            else:
                print("No Inventory Exists")
                time.sleep(2)
            menu_one(session.inventories, session)
            return
        case _ if user_choice == create_index:
            create_inventory()
            if session.signed_in:
                save_all(session.get_user(), session.inventories)
            menu_one(session.inventories, session)
            return
        case _ if user_choice in number_name_pair:
            menu_two(session.inventories, number_name_pair[user_choice])
            return
        case _:
            print("Invalid Selection")
            time.sleep(2)
            menu_one(session.inventories, session)
            return

def menu_two(invent: session.inventories, invent_name): #Categories
    """
    Second level, categories level, shows all categories

    :param invent: the active inventories dict
    :type invent: dict
    :param invent_name: the open inventory name
    :type invent_name: str
    """
    clear_screen()
    count = 1
    curr_cate = invent[invent_name].get_categories()
    for cate in curr_cate:
        print(f'{count}. {cate.get_name()}')
        count = count + 1
    print(f'{count}. Create Category')
    count = count + 1
    print(f'{count}. Delete Category')
    count = count + 1
    print(f'{count}. Input Sales')
    count = count + 1
    print(f'{count}. Display Profit and Revenue')
    count = count + 1
    print(f'{count}. Generate Sales Report')
    count = count + 1
    print(f'{count}. Back')

    create_index = count - 5
    delete_index = count - 4
    sales_index = count - 3
    display_index = count - 2
    report_index = count - 1
    back_index = count
    num_categories = len(curr_cate)

    user_choice = input("Enter Corresponding Number: ")
    while (bool(re.search(r"\D", user_choice)) or user_choice == ""):
        user_choice = input("Invalid. Enter Corresponding Number: ")
    user_choice = int(user_choice)

    match(user_choice):
        case _ if user_choice == create_index:
            create_category(session.inventories, invent_name)
            if session.signed_in:
                save_all(session.get_user(), session.inventories)
            menu_two(session.inventories, invent_name)
            return
        case _ if user_choice == delete_index:
            if curr_cate:
                delete_category(session.inventories, invent_name)
                if session.signed_in:
                    save_all(session.get_user(), session.inventories)
            else:
                print("No Category Exists")
                time.sleep(2)
            menu_two(session.inventories, invent_name)
            return
        case _ if user_choice == sales_index:
            invent_purchase(session.inventories, invent_name)
            if session.signed_in:
                save_all(session.get_user(), session.inventories)
            menu_two(session.inventories, invent_name)
            return    
        case _ if user_choice == display_index:
            clear_screen()
            print(f'Revenue: {invent[invent_name].get_revenue()}\nProfit: {invent[invent_name].get_profit()}')
            print("\n1. Back")
            while True:
                user_choice = input("Enter 1 to go back: ")
                try:
                    choice = int(user_choice)
                    if choice == 1:
                        break
                except ValueError:
                    print("Invalid. Enter a number for price:")
            menu_two(session.inventories, invent_name)
            return
        case _ if user_choice == report_index:
            clear_screen()
            create_report(session.inventories, invent_name)
            print("Report Generated.")
            print(invent[invent_name].get_pro_sold_dict())
            print(invent[invent_name].get_cate_sold_dict())
            time.sleep(5)
            menu_two(session.inventories, invent_name)
        case _ if user_choice == back_index:
            menu_one(session.inventories, session)
            return
        case _ if 1 <= user_choice <= num_categories:
            menu_three(invent_name, curr_cate[user_choice-1].get_products(), curr_cate[user_choice-1].get_name())
            return
        case _:
            print("Invalid Input")
            time.sleep(2)
            menu_two(session.inventories, invent_name)
            return

def menu_three(invent_name, products, cate_name): #Products
    """
    Third level, products level, shows all products

    :param invent_name: name of current inventory
    :type invent_name: str
    :param products: list of products within category
    :type products: array
    :param cate_name: the open category name
    :type cate_name: str
    """
    clear_screen()
    products = get_category(session.inventories, invent_name, cate_name).get_products()
    count = 1
    for pro in products:
        print(f'{count}. {pro.get_name()}')
        count = count + 1
        curr_pro.append(pro)
    
    print(f'{count}. Create Product')
    count = count + 1
    print(f'{count}. Delete Product')
    count = count + 1
    print(f'{count}. Back')

    create_index = count - 2
    delete_index = count - 1
    back_index = count
    num_products = len(products)

    user_choice = input("Enter Corresponding Number: ")
    while (bool(re.search(r"\D", user_choice)) or user_choice == ""):
        user_choice = input("Invalid. Enter Corresponding Number: ")
    user_choice = int(user_choice)

    match(user_choice):
        case _ if user_choice == create_index:
            create_product(session.inventories, invent_name, cate_name)
            if session.signed_in:
                save_all(session.get_user(), session.inventories)
            menu_three(invent_name, curr_pro, cate_name)
            return
        case _ if user_choice == delete_index:
            print('Delete index')
            if products:
                pro_name_id = input("Enter Product Name or ID: ")
                delete_product(session.inventories, invent_name, cate_name, pro_name_id)
                if session.signed_in:
                    save_all(session.get_user(), session.inventories)
            else:
                print("No Product Exists")
                time.sleep(2)
            menu_three(invent_name, curr_pro, cate_name)
            return
        case _ if user_choice == back_index:
            menu_two(session.inventories, invent_name)
            return
        case _ if 1 <= user_choice <= num_products:
            menu_four(products[user_choice-1], invent_name, cate_name)
            return
        case _:
            print("Invalid Input")
            time.sleep(2)
            menu_three(invent_name, curr_pro, cate_name)
            return

def menu_four(product, invent_name, cate_name): #Product Info
    """
    Fourth level, product level, shows product detail
    
    :param product: the product that is currently open
    :type product: Product class
    :param invent_name: name of the current inventory 
    :type invent_name: str
    :param cate_name: name of the current category 
    :type cate_name: str
    """
    clear_screen()
    print(product)

    count = 1
    print(f'{count}. Change Name')
    count = count + 1
    print(f'{count}. Change Price')
    count = count + 1
    print(f'{count}. Add Supply')
    count = count + 1
    print(f'{count}. Remove Supply')
    count = count + 1
    print(f'{count}: Back')

    change_na_index = count - 4
    change_price_index = count - 3
    add_index = count - 2
    remove_index = count - 1
    back_index = count

    user_choice = input("Enter Corresponding Number: ")
    while (bool(re.search(r"\D", user_choice)) or user_choice == ""):
        user_choice = input("Invalid. Enter Corresponding Number: ")
    user_choice = int(user_choice)

    match(user_choice):
        case _ if user_choice == change_na_index:
            clear_screen()
            new_name = input("Enter new name: ")
            product.change_name(new_name)
            if session.signed_in:
                save_all(session.get_user(), session.inventories)
            menu_four(product, invent_name, cate_name)
            return
        case _ if user_choice == change_price_index:
            clear_screen()

            while True:
                new_price = input("New Price: ")
                try:
                    new_price = float(new_price)
                    break
                except ValueError:
                    print("Invalid. Enter a number: ")

            product.change_cost(new_price)
            if session.signed_in:
                save_all(session.get_user(), session.inventories)
            menu_four(product, invent_name, cate_name)
            return
        case _ if user_choice == add_index:
            clear_screen()

            while True:
                add_supply = input("Amount to Add: ")
                try:
                    add_suply = int(add_supply)
                    break
                except ValueError:
                    print("Invalid. Enter a integer please.")

            product.add_supply(add_supply)
            if session.signed_in:
                save_all(session.get_user(), session.inventories)
            menu_four(product, invent_name, cate_name)
            return
        case _ if user_choice == remove_index:
            clear_screen()

            while True:
                remove = input("Amount to Remove: ")
                try:
                    remove = int(remove)
                    if product.get_supply() >= remove:
                        break
                    else:
                        print("Invalid. Not enough supply.")
                except ValueError:
                    print("Invalid. Not integer. ")

            product.remove_supply(int(remove))
            if session.signed_in:
                save_all(session.get_user(), session.inventories)
            menu_four(product, invent_name, cate_name)
            return
        case _ if user_choice == back_index:
            clear_screen()
            menu_three(invent_name, curr_pro, cate_name)
            return
        case _:
            print("Invalid Input")
            time.sleep(2)
            menu_four(pro_name_id, invent_name, cate_name)
            return
            
#Start of program
menu_one(session.inventories, session)