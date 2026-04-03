"""
This module provides classes and functions to:
 - Control inventory, category, and products.
 - Tracks profit and revenue of inventory.
 - Runs sales that occur for products.

Author: Kaipo Ojas
Date: 2026-03-20 (Ended not started)
"""
import random
#cd folderName then python fileName.py to run

id_list = {} #{cate: [id, name]}
sold_pro = {} #{product name: num sold}
sold_cate = {} #{category name: num sold}

class MasterClass:
    """
    Single inventory class. Has it's own profit and revenue.
    """

    #========built-in methods========
    def __init__(self, **cate):
        """
        Initialize the inventory class.

        :param cate: Categories to intially add to inventory
        :type cate: array
        """
        self.categories = []
        for category in list(cate):
            self.categories.append(category)
        self.profit = 0.00
        self.revenue = 0.00
            
    def __str__(self):
        """
        Returns string of categories within a inventory
        """
        return ", ".join(cate.get_name() for cate in self.categories)

    #========get methods============
    def get_profit(self):
        """
        Gets inventory profit.

        :return: returns profit
        :rtype: double
        """
        return self.profit
    
    def get_revenue(self):
        """
        Gets inventory revenue

        :return: returns revenue
        :rtype: double
        """
        return self.revenue

    #=====Setter Methods===========
    def set_profit(self, p):
        """
        Sets new value for inventory profit.

        :param p: new profit value
        :type p: double or int
        """
        self.profit = p
    
    def set_revenue(self, r):
        """
        Sets new value for inventory revenue.

        :param r: new revenue value
        :type r: double or int
        """
        self.revenue = r
    
    def get_categories(self):
        """
        Gets categories list for inventory.
        
        :return: array of categories classes
        :rtype: array
        """
        return self.categories
    
    def get_pro_sold_dict(self):
        """
        Dict of product and amount sold.

        :return: the sold product dict.
        :rtype: dict.
        """
        return sold_pro

    def get_cate_sold_dict(self):
        """
        Dict of category and amount sold.

        :return: the sold category dict.
        :rtype: dict
        """
        return sold_cate

    #=======Category========
    def get_category(self, cate_name):
        """
        Returns the category with corresponding name.

        :param cate_name: the category name of which to return.
        :type cate_name: str

        :return: category class of matching name or Not Found
        :rtype: Category class or str
        """
        for cate in self.categories:
            if cate.get_name() == cate_name:
                return cate
        return "Not Found"

    def find_category(self, cate_name):
        """
        Find and returns whether a category of given name exist.

        :param cate_name: category name of one to look for.
        :type cate_name: str
        :return: Returns true or false depending if category was found.
        :rtype: bool
        """
        for cate in self.categories:
            if cate.get_name() == cate_name:
                return True
        return False

    def create_category(self, name):
        """
        Creates a category then adds to category list.

        :param name: name of new category.
        :type name: str
        """
        self.categories.append(Category(name, self))
        sold_cate.setdefault(name, 0)
    
    def remove_category(self, name):
        """
        Removes category with corresponding name.

        :param name: name of category to remove
        :type name: str
        """
        self.categories = [cate for cate in self.categories if cate.get_name() != name]
    
    #======Product=======
    def has_product(self, name_or_id):
        """
        Checks whether inventory contains certain product
        :param name_or_id: the name or product id of one to seek.
        :type name_or_id: str
        :return: returns whether found product or not
        :rtype: str
        """
        for cate_name, products in id_list.items():
            for pro in products:
                if pro["id"] == name_or_id or pro["name"] == name_or_id:
                    return "Found"
        return "Not Found"
    
    def get_product(self, name_or_id):
        """
        Returns product class with corresponding name or id.

        :param name_or_id: the name or id of product to return.
        :type name_or_id: str
        :return: The corresponding product class or Not Found
        :rtype: Product class or str
        """
        for cate_name, products in id_list.items():
            for pro in products:
                if pro["id"] == name_or_id or pro["name"] == name_or_id:
                    return self.get_category(cate_name).get_product(name_or_id)
        return "Not Found"

    #======Add=======
    def add_costs(self, amount):
        """
        Adds a cost which cuts into profit.
        :param amount: Amount of cost
        :type amount: double or int
        """
        print(amount)
        self.profit -= amount
    
    def add_sale(self, amount):
        """
        Adds sale amount to profit and revenue

        :param amount: amount to add to profit and revenue
        :type amount: double or int
        """
        self.profit += amount
        self.revenue += amount
        print(self.profit)

    def purchased(self, name_or_id, sold):
        """
        Inventory level sales runner.

        :param name_or_id: Name or id of the sold product
        :type name_or_id: str
        :param sold: number sold for given product
        :type sold: int
        :return: only returns something if product was not found
        :rtype: str
        """
        for cate_name, products in id_list.items():
            for pro in products:
                if pro["id"] == name_or_id or pro["name"] == name_or_id:
                    print("Found Product")
                    self.get_category(cate_name).purchased(name_or_id, sold)
                    self.add_sale(sold * self.get_product(name_or_id).get_price()) 
                    sold_pro[pro["name"]] += sold   
                    sold_cate[cate_name] += sold
                    return
        return "Not Found"

#===================

class Category(MasterClass):
    """
    Category level, stored in the Inventory class.
    Child of the MasterClass(InventoryClass)

    Tracks product within that category.
    """
    #built-in methods
    def __init__(self, na, inventory):
        """
        Intialize Category class

        :param na: name of category
        :type na: str
        :param inventory: parent inventory class
        :type inventory: MasterClass class
        """
        self.products = []
        self.name = na
        self.inventory = inventory
    
    def __str__(self):
        """
        String method

        :return: returns each of product name in category.
        :rtype: str
        """
        return ", ".join(pro.get_name() for pro in self.products)

    #========get methods==========
    def get_name(self):
        """
        Gets the name of the Category

        :return: returns the category name.
        :rtype: str
        """
        return self.name
    
    def get_product(self, name_or_id):
        """
        Returns the Product class with corresponding name

        :param name_or_id: name or id of the product to return
        :type name_or_id: str or int
        :return: returns the product class or Not Found
        :rtype: Product class or str
        """
        for pro in self.products:
            if pro.get_id() == name_or_id or pro.get_name() == name_or_id:
                return pro
        return "Not Found"
    
    def get_products(self):
        """
        Returns list of product objects.

        :return: list of products contained the Category
        :rtype: array
        """
        return self.products

    def get_profit(self):
        """
        Returns the current profit of the inventory

        :return: profit of current inventory
        :rtype: double
        """
        return self.profit        

    #========Product==========
    def create_product(self, n, a, c, paid, cate_name, i=None):
        """
        Creates product object with given name, supply, cost, aquistion cost.

        :param n: name of product
        :type n: str
        :param a: amount/supply of product
        :type a: int
        :param c: cost of one product
        :type c: double
        :param paid: Acquistion cost for one product.
        :type paid: double
        :param cate_name: the category name of which the product is child of
        :type cate_name: str
        :param i: The id to assign product, only if product didn't exist prior
        :type i: int
        """
        if i == None:
            self.products.append(Product(n, a, c, cate_name))
        else:
            self.products.append(Product(n, a, c, cate_name, i))
        self.inventory.add_costs(paid * a)
        sold_pro.setdefault(n, 0)
    
    def remove_product(self, na_or_id):
        """
        Removes product object from products list

        :param na_or_id: name or id of the product to remove.
        :type na_or_id: str or int
        """
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

    def add_supply_to_product(self, id, supply, paid):
        """
        Adds supply to corresponding product.
        :param id: id of the product to add supply to.
        :type id: int
        :param supply: Amount to add to supply
        :type supply: int
        :param paid: Amount paid for each product.
        :type paid: double
        """
        for pro in self.products:
            if pro.get_id() == id:
                pro.add_supply(supply)
                break
        pro.add_supply(supply)
        self.profit = self.profit - (paid * supply) 
    
    def remove_supply_from_product(self, id, supply):
        """
        Removes supply from product(not sold).

        :param id: id of the product to remove supply from.
        :type id: int
        :param supply: Amount to remove from supply.
        :type supply: int
        """
        for pro in self.products:
            if pro.get_id() == id:
                pro.remove_supply(supply)
                break
    
    def change_cost(self, name_or_id, new_cost):
        """
        Modifies to cost of product.

        :param name_or_id: Name or id of the product to change price for.
        :type name_or_id: str or int
        :param new_cost: New cost to set product to
        :type new_cost: double
        """
        for pro in self.products:
            if name_or_id == pro.get_name() or name_or_id == pro.get_id():
                pro.change_cost(new_cost)
    
    def purchased(self, name_or_id, supply):
        """
        Purchased, Category Level, called on product level

        :param name_or_id: Name or id of the sold product
        :type name_or_id: str or int
        :param supply: amount of product sold
        :type supply: int
        """
        for pro in self.products:
            if pro.get_id() == name_or_id or pro.get_name() == name_or_id:
                pro.purchased(supply)


#========Product===========

class Product(Category):
    """
    Product class, child of Category class.
    Represents a single product.
    """
    #built-in methods  
    def __init__(self, n, s, c, cate_name, id=None):
        """
        Intialization of product.
        :param n: name of product
        :type n: str
        :param s: supply/amount have of product.
        :type s: int
        :param c: Cost/Price of product
        :type c: double
        :param cate_name: Name of category which product is child of.
        :type cate_name: str
        :param id: id to set product to, if None then new rnadomly generated.
        :type id: int
        """
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
        """
        String of Product
        :return: returns name, id, supply, and price of product.
        :rtype: str
        """
        return f"Name: {self.name}\nID: {self.id}\nSupply: {self.supply}\nCost: {self.cost:.2f}\n"

    #=========get methods=======
    def get_name(self):
        """
        Gets name of product
        
        :return: name of product
        :rtype: str
        """
        return self.name
    
    def get_id(self):
        """
        Gets id of product

        :return id of product
        :rtype: int
        """
        return self.id
    
    def get_cost(self):
        """
        Gets cost of one product

        :return: returns the cost of product
        :rtype: double
        """
        return self.cost
    
    def get_supply(self):
        """
        Gets current supply amount of product.

        :return: supply of product
        :rtype: int
        """
        return self.supply
    
    def get_price(self):
        """
        Gets price of product.

        :return: price of one product.
        :rtype: double
        """
        return self.cost
    
    #=======Modify=======
    def add_supply(self, add):
        """
        Adds to supply of product

        :param add: amount to add
        :type add: int
        """
        self.supply = self.supply + add

    def remove_supply(self, remove):
        """
        Remove from supply of product

        :param remove: Amount to remove
        :type remove: int
        """
        self.supply = self.supply - remove

    def change_cost(self, new_cost):
        """
        Modify cost/price of product

        :param new_cost: new cost to set product to.
        :type new_cost: double
        """
        self.cost = new_cost

    def change_name(self, new_name):
        """
        Modify the name of product

        :param new_name: New name to set product to
        :type new_name: str
        """
        self.name = new_name
              
    def purchased(self, supply):
        """
        Purchased.

        :param supply: Amount of product sold
        :type supply: int
        """
        self.remove_supply(supply)