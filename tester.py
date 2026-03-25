import json          # Used to store/load user data from a file
import bcrypt       # Used for secure password hashing
from main import MasterClass, Category, Product

DB_FILE = "users.json"   # File where all user data will be saved


# -------------------------
# LOAD DATABASE FROM FILE
# -------------------------
try:
    # Try to open and load existing user data
    with open(DB_FILE, "r") as f:
        db = json.load(f)
except:
    # If file doesn't exist yet, start with empty database
    db = {}


# -------------------------
# SAVE DATABASE TO FILE
# -------------------------
def save_db():
    """
    Writes the current database (db dictionary)
    to the JSON file so it persists after program closes
    """
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)  # indent=4 makes it readable


# -------------------------
# SIGNUP FUNCTION
# -------------------------
def signup(username, password):
    """
    Creates a new user account
    - Stores hashed password (NOT plain text)
    - Initializes empty inventory
    """

    # Check if username already exists
    if username in db:
        print("User already exists")
        return

    # Convert password string → bytes (required by bcrypt)
    password_bytes = password.encode()

    # Generate salt + hash the password
    # bcrypt automatically handles salting internally
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # Store user data in database
    db[username] = {
        "hash": hashed.decode(),   # store as string so JSON can save it
        "inventory": {}            # start with empty inventory
    }

    # Save changes to file
    save_db()

    print("Account created!")


# -------------------------
# LOGIN FUNCTION
# -------------------------
def login(username, password):
    """
    Verifies a user's login credentials
    Returns the user's data if successful
    """

    # Check if username exists
    if username not in db:
        print("User not found")
        return None

    # Get stored hash and convert back to bytes
    stored_hash = db[username]["hash"].encode()

    # Convert entered password to bytes
    password_bytes = password.encode()

    # Compare entered password with stored hash
    # bcrypt handles salt internally during comparison
    if bcrypt.checkpw(password_bytes, stored_hash):
        print("Login successful!")
        return db[username]   # return user data (inventory, etc.)
    else:
        print("Wrong password")
        return None


# -------------------------
# ADD ITEM TO INVENTORY
# -------------------------
def add_item(user, item):
    """
    Adds an item to the logged-in user's inventory
    """

    # Append item (dictionary) to inventory list
    #user["inventory"].append(item)

    # Save updated database
    save_db()

def save_all(user, inventory):
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

# -------------------------
# VIEW INVENTORY
# -------------------------
def view_inventory(user):
    """
    Prints all items in user's inventory
    """

    if not user["inventory"]:
        print("Inventory is empty")
        return

    print("\nInventory:")
    for item in user["inventory"]:
        print(item)

inventories = {
    "Invent1": MasterClass()
}
  
def load_all(user):
    for invent_name, invent_inner_dict in user["inventory"].items():
        inventories.setdefault(invent_name, MasterClass())
        for cate_name, cate_inner_dict in invent_inner_dict.items():
            if cate_name == "Profit":
                inventories[invent_name].set_profit(cate_inner_dict)
            elif cate_name == "Revenue":
                inventories[invent_name].set_revenue(cate_inner_dict)
            else:
                inventories[invent_name].create_category(cate_name)
                for pro_name, pro_info in cate_inner_dict.items():
                    if len(pro_info) == 3:
                        inventories[invent_name].get_category(cate_name).create_product(pro_name, pro_info[1], pro_info[0], 0, cate_name, pro_info[2])
                    else:
                        inventories[invent_name].get_category(cate_name).create_product(pro_name, pro_info[1], pro_info[0], 0, cate_name)


# -------------------------
# MAIN PROGRAM (TEST FLOW)
# -------------------------

# Create a new account
signup("A", "1234")

# Attempt login
user = login("A", "1234")

# If login successful, allow actions
if user:
    # Add items

    inventories["Invent1"].create_category("Food")
    save_all(user, inventories)
    category = inventories["Invent1"].get_category("Food")
    save_all(user, inventories)
    if user.get("Invent1") and "Apple" in user["Invent1"]:
        category.create_product("Apple", 100, 1.00, 0.25, "Food", user["inventory"]["Invent1"]["Food"]["Apple"][2])     
    else:
        category.create_product("Apple", 100, 1.00, 0.25, "Food")
    save_all(user, inventories)

    #load_all(user)

    # View inventory
    view_inventory(user)

