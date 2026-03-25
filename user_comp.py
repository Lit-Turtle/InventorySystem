#Kaipo Ojas

from main import MasterClass, Category, Product
import os
import time
import re
import json
import bcrypt

#Class to track user and inventory
class Session:
    def __init__(self, user=None, signed_in=False):
        self.user = user
        self.signed_in = signed_in
        self.inventories = {}
    
    def logged_out(self):
        self.signed_in = False
        self.user = None
    
    def logged_in(self, user):
        self.user = user
        self.signed_in = True
    
    def get_user(self):
        return self.user
    
    def set_user(self, u):
        self.user = u

session = Session(None, None)

curr_cate = []
curr_pro = []

#Clears console
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#=============Basic Inventory Methods============

#Gets inventory name and adds inventory object to list
def create_inventory():
    clear_screen()
    invent_name = input("Inventory Name: ")
    session.inventories.setdefault(invent_name, MasterClass())

#Asks for inventory name and deletes inventory with corresponding name
def delete_inventory(invent: session.inventories):
    clear_screen()
    invent_name = input("Inventory Name: ")
    if invent_name in session.inventories:
        del session.inventories[invent_name]

#Finds category in inventory and returns whether inventory exists
def find_category(invent: session.inventories, invent_name, cate_name):
    return invent[invent_name].find_category(cate_name)

#Finds category in inventory and returns Category object with corresponding name
def get_category(invent: session.inventories, invent_name, cate_name):
    return invent[invent_name].get_category(cate_name)

#Asks for category name and creates a Category object with corresponding name
def create_category(invent: session.inventories, invent_name):
    clear_screen()
    cate_name = input("Category Name: ")
    invent[invent_name].create_category(cate_name)

#Asks for category name and deletes Category object with corresponding name
def delete_category(invent: session.inventories, invent_name):
    clear_screen()
    cate_name = input("Category Name to Delete: ")
    invent[invent_name].remove_category(cate_name)

#Not Needed or used also method does not exist****
def delete_index(invent:session.inventories, invent_name):
    clear_screen()
    cate_name = input("Category to Delete: ")
    invent[invent_name].delete_category(cate_name)

#Creates product with given inventory name and category name
def create_product(invent: session.inventories, invent_name, cate_name, id=None):
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
    
#Deletes product in corresponding category and name or id(Can remake this with new Master get_product)
def delete_product(invent: session.inventories, invent_name, cate_name, pro_name_id):
    get_category(invent, invent_name, cate_name).remove_product(pro_name_id)

#Seems to grab products list from category: but not used****
def update_products(cate_name):
    for cate in curr_cate:
        if cate.get_name() == cate_name:
            return cate.get_products()

#Returns Product object in correspding category and name or id
def get_product(invent_name, cate_name, pro_name_id):
    return get_category(session.inventories, curr_cate[teste_met()].get_products(), cate_name).get_product(pro_name_id)

#Category level purchase
def purchased(invent: session.inventories, invent_name, cate_name):
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

#Procceses purchases with just inventory name
def invent_purchase(invent: session.inventories, invent_name):
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

#Generates a report in Sales Report.txt
def create_report(invent: session.inventories, invent_name):
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

#Saves database to file
def save_db():
    with open(db_file, "w") as f:
        json.dump(db, f, indent=4)

#Creates account and saves whatever inventory currently had made
def create_account():
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

#Lets user login to account
def login():
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

#Saves inventory to json database file
def save_all(user, inventory):
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

#Shows inventory
def view_inventory():
    if not user["inventory"]:
        print("Inventory Empty")
        return 
    
    print("\nInventory")
    for item in user["inventory"]:
        print(item)

#Loads data from json file
def load_all(user):
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

def menu_one(invent: session.inventories, session): #session.inventories
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
