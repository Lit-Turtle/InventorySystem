#Kaipo Ojas

import random
#cd folderName then python fileName.py to run

id_list = {} #{cate: [id, name]}
sold_pro = {} #{product name: num sold}
sold_cate = {} #{category name: num sold}

class MasterClass:
    #id_list = []

    #========built-in methods========
    def __init__(self, **cate):
        self.categories = []
        for category in list(cate):
            self.categories.append(category)
        self.profit = 0.00
        self.revenue = 0.00
            
    def __str__(self):
        return ", ".join(cate.get_name() for cate in self.categories)

    #========get methods============
    #Returns profit of inventory
    def get_profit(self):
        return self.profit
    
    #Returns revenue of inventory
    def get_revenue(self):
        return self.revenue

    #=====Setter Methods===========
    def set_profit(self, p):
        self.profit = p
    
    def set_revenue(self, r):
        self.revenue = r
    
    #Returns a list of all categories objects in inventory
    def get_categories(self):
        return self.categories
    
    def get_pro_sold_dict(self):
        return sold_pro

    def get_cate_sold_dict(self):
        return sold_cate

    #=======Category========
    #Returns category object with corresponding name unless not found
    def get_category(self, cate_name):
        for cate in self.categories:
            if cate.get_name() == cate_name:
                return cate
        return "Not Found"

    #Checks and returns whether a category with corresponding name exists
    def find_category(self, cate_name):
        for cate in self.categories:
            if cate.get_name() == cate_name:
                return True
        return False

    #Creates a category obejct with corresponding name
    def create_category(self, name):
        self.categories.append(Category(name, self))
        sold_cate.setdefault(name, 0)
    
    #Removes a category with corresponding name
    def remove_category(self, name):
        self.categories = [cate for cate in self.categories if cate.get_name() != name]
    
    #======Product=======
    #Checks whether and returns whether products exists
    def has_product(self, name_or_id):
        for cate_name, products in id_list.items():
            for pro in products:
                if pro["id"] == name_or_id or pro["name"] == name_or_id:
                    return "Found"
        return "Not Found"
    
    #Gets and returns Product object with corresponding name or id
    def get_product(self, name_or_id):
        for cate_name, products in id_list.items():
            for pro in products:
                if pro["id"] == name_or_id or pro["name"] == name_or_id:
                    return self.get_category(cate_name).get_product(name_or_id)
        return "Not Found"

    #======Add=======
    #Removes cost from profit
    def add_costs(self, amount):
        print(amount)
        self.profit -= amount
    
    #Takes sales money and adds to profit and revenue
    def add_sale(self, amount):
        self.profit += amount
        self.revenue += amount
        print(self.profit)

    #Inputs purchases in terms of supply and profits taking pro name or id and amount
    def purchased(self, name_or_id, sold):
        for cate_name, products in id_list.items():
            for pro in products:
                if pro["id"] == name_or_id or pro["name"] == name_or_id:
                    print("Found Profuct")
                    self.get_category(cate_name).purchased(name_or_id, sold)
                    self.add_sale(sold * self.get_product(name_or_id).get_price()) 
                    sold_pro[pro["name"]] += sold   
                    sold_cate[cate_name] += sold
                    return
        return "Not Found"

#===================

class Category(MasterClass):
    
    #built-in methods
    def __init__(self, na, inventory):
        self.products = []
        self.name = na
        self.inventory = inventory
    
    def __str__(self):
        return ", ".join(pro.get_name() for pro in self.products)

    #========get methods==========
    #Returns Category name
    def get_name(self):
        return self.name
    
    #Returns Product object with corresponding name
    def get_product(self, name_or_id):
        for pro in self.products:
            if pro.get_id() == name_or_id or pro.get_name() == name_or_id:
                return pro
        return "Not Found"
    
    #Returns list of product objects
    def get_products(self):
        return self.products

    #Get Inventory Profit
    def get_profit(self):
        return self.profit        

    #========Product==========
    #Creates product object with given name, supply, cost, aquistion cost
    def create_product(self, n, a, c, paid, cate_name, i=None):
        if i == None:
            self.products.append(Product(n, a, c, cate_name))
        else:
            self.products.append(Product(n, a, c, cate_name, i))
        #self.profit = self.profit - (paid * a)
        self.inventory.add_costs(paid * a)
        sold_pro.setdefault(n, 0)
    
    #Removes product object from products list
    def remove_product(self, na_or_id):
        global id_list
        self.products = [pro for pro in self.products if pro.get_name() != na_or_id and pro.get_id() != na_or_id]
        for cate, products in id_list.items():
            id_list[cate] = [
                item for item in products
                if item["id"] != na_or_id and item["name"] != na_or_id
            ]

    # Remove from id_list
    for cate in id_list:
        # If input is ID
        if isinstance(na_or_id, int):
            id_list[cate].pop(na_or_id, None)

        # If input is name
        else:
            # Find matching ID(s) for that name
            ids_to_remove = [
                pid for pid, name in id_list[cate].items()
                if name == na_or_id
            ]
            for pid in ids_to_remove:
                id_list[cate].pop(pid, None)

    #Adds supply to product
    def add_supply_to_product(self, id, supply, paid):
        for pro in self.products:
            if pro.get_id() == id:
                pro.add_supply(supply)
                break
        pro.add_supply(supply)
        self.profit = self.profit - (paid * supply) 
    
    #Removes supply from product(not sold)
    def remove_supply_from_product(self, id, supply):
        for pro in self.products:
            if pro.get_id() == id:
                pro.remove_supply(supply)
                break
    
    #Modify Cost of product
    def change_cost(self, name_or_id, new_cost):
        for pro in self.products:
            if name_or_id == pro.get_name() or name_or_id == pro.get_id():
                pro.change_cost(new_cost)
    
    #Purchased, Category Level, called on product level
    def purchased(self, name_or_id, supply):
        for pro in self.products:
            if pro.get_id() == name_or_id or pro.get_name() == name_or_id:
                pro.purchased(supply)
                #self.inventory.add_sale(supply * pro.get_cost())


#========Product===========

class Product(Category):
    #built-in methods  
    def __init__(self, n, s, c, cate_name, id=None):
        self.name = n
        self.supply = s
        self.cost = c 
        if id == None:
            self.id = ''.join(str(random.randint(0, 9)) for _ in range(5))
            #Supposed to regenerate if code already exists
            while any(len(li) > 0 and self.id == li[0] for li in id_list.values()):
                self.id = ''.join(str(random.randint(0, 9)) for _ in range(5))
        else:
            self.id = id
        print(f'{self.name}: {self.id}')
        id_list.setdefault(cate_name, []).append({
            "id": self.id,
            "name": n
        })
        #id_list.append(self.id)
    
    def __str__(self):
        return f"Name: {self.name}\nID: {self.id}\nSupply: {self.supply}\nCost: {self.cost:.2f}\n"

    #=========get methods=======
    #Returns name of product
    def get_name(self):
        return self.name
    
    #Returns id num of product
    def get_id(self):
        return self.id
    
    #Returns the acqusition cost of product
    def get_cost(self):
        return self.cost
    
    #Returns remaining supply of product
    def get_supply(self):
        return self.supply
    
    #Returns price of product
    def get_price(self):
        return self.cost
    
    #=======Modify=======
    #Adds supply to product 
    def add_supply(self, add):
        self.supply = self.supply + add

    #Removes supply from product
    def remove_supply(self, remove):
        self.supply = self.supply - remove

    #Modify Cost
    def change_cost(self, new_cost):
        self.cost = new_cost

    def change_name(self, new_name):
        self.name = new_name
              
    #Purchased
    def purchased(self, supply):
        self.remove_supply(supply)
        #self.profit = self.profit + (supply * self.cost)
        #self.revenue = self.revenue + (supply * self.cost)
        #self.add_sale(supply * self.cost)
