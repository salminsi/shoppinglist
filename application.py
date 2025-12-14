# You can initialize the MongoDB client here so it is available for every function in this file
from pymongo import MongoClient
from bson.objectid import ObjectId

#yhdistä mongodb
client = MongoClient("mongodb://localhost:27017/")

#uusi tietokanta
db = client["shoppingdatabase"]

#kokoelmat
shoppinglists_col = db["shoppinglists"]
products_col = db["products"]

#uusi dokumentti
shoppinglists = {
    "name": "UusiVuosi",
    "store": "HalpaHalli",
    "isCompleted": False
}

shoppinglists_result = shoppinglists_col.insert_one(shoppinglists)
shoppinglists_id = shoppinglists_result.inserted_id

print("Shoppinglist added, id: ", shoppinglists_id)

#lisää tuotteita ostoslistalle
products = [
    {
        "name": "ChiliNuts",
        "brand": "Taffel",
        "quantity": 1,
        "tags": ["Nuts", "Snacks"],
        "isPurchased": False,
        "shoppinglist_id": shoppinglists_id
    },
    {
        "name": "OriginalChips",
        "brand": "Estrella",
        "quantity": 2,
        "tags": ["Chips", "Snacks"],
        "isPurchased": False,
        "shoppinglist_id": shoppinglists_id
    }
]

products_col.insert_many(products)
print("Products added")


#Valikko
print("Welcome to the shoppinglist application!")

def print_commands():
    print("Commands:")
    print("\t1) List shoppinglists")
    print("\t2) Add a shoppinglist")
    print("\t3) Edit a shoppinglist")
    print("\t4) Delete a shoppinglist") 
    print("\t5) List products")
    print("\t6) Add a product")
    print("\t7) Edit a product")
    print("\t8) Delete a product")
    print("\t9) Exit application")
    

def add_shoppinglists():
    print("\nProvide the shoppinglist's information")
    name = input("Name:")
    store = input("Store:")
    isCompleted_input = input("Is completed? (yes/no): ").strip().lower()
    isCompleted = True if isCompleted_input in ["yes", "y"] else False
   
    # Insert the shoppinglist into the database
    shoppinglists = {
    "name": name,
    "store": store,
    "isCompleted": isCompleted
    }
        
    result = shoppinglists_col.insert_one(shoppinglists)
    print(f"\nShoppinglist '{name}' has been added with id: {result.inserted_id}")

def list_shoppinglists():
    # Find all the shoppinglists from the database and print their information
    shoppinglists = shoppinglists_col.find()
    print("\nShoppinglists:")
    for sl in shoppinglists:
        print("\nID:", sl["_id"])
        print("Name:", sl["name"])
        print("Store:", sl["store"])
        print("Completed:", sl["isCompleted"])

def edit_shoppinglists():
    print("\nWhich shoppinglist do you want to edit?")
    shoppinglists_id_input = input("Shoppinglist ID:")
    print("\nProvide the new information for the shoppinglist")
    # Request new values for the shoppinglist's fields from the user and update them based on the shoppinglist's id
    try:
        shoppinglist_objid = ObjectId(shoppinglists_id_input)
    except:
        print("Invalid ID format")
        return
    
    sl = shoppinglists_col.find_one({"_id": shoppinglist_objid})
    
    name = input(f"\nNew name [{sl['name']}]: ") or sl['name']
    store = input(f"New store [{sl['store']}]: ") or sl['store']
    isCompleted_input = input(f"Is completed? (yes/no) [{sl['isCompleted']}]: ").strip().lower()
    isCompleted = sl['isCompleted'] 
    if isCompleted_input in ["yes", "y"]:
        isCompleted = True
    elif isCompleted_input in ["no", "n"]:
        isCompleted = False

    # Päivitä dokumentti
    shoppinglists_col.update_one(
        {"_id": shoppinglist_objid},
        {"$set": {"name": name, "store": store, "isCompleted": isCompleted}}
    )

    print("Shoppinglist updated.")

def delete_shoppinglists():
    # Request shoppinglist's id from the user and delete it
    print("\nWhich shoppinglist do you want to delete?")
    shoppinglists_id_input = input("Shoppinglist ID:")
    try:
        shoppinglist_objid = ObjectId(shoppinglists_id_input)
    except:
        print("Invalid ID format")
        return
    
    # Poista ostoslista
    result = shoppinglists_col.delete_one({"_id": shoppinglist_objid})
    
    # Poista myös kaikki ostoslistan tuotteet
    products_result = products_col.delete_many({"shoppinglist_id": shoppinglist_objid})

    print(f"Shoppinglist deleted. {products_result.deleted_count} products also deleted.")
    

def add_products():
    print("\nProvide the product's information")
    name = input("Name:")
    brand = input("Brand:")
    quantity = input("Quantity:")
    tags_input = input("Tags (comma separated):")
    tags = [t.strip() for t in tags_input.split(",") if t.strip()]
    isPurchased_input = input("Is purchased? (yes/no): ").strip().lower()
    isPurchased = True if isPurchased_input in ["yes", "y"] else False
    shoppinglists_id = input("Shoppinlist ID:")
    try:
        shoppinglist_objid = ObjectId(shoppinglists_id)
    except:
        print("Invalid Shoppinglist ID format!")
        return
    
    # Insert the product into the database
    products = {
    "name": name,
    "brand": brand,
    "quantity": quantity,
    "tags": tags,
    "isPurchased": isPurchased,
    "shoppinglist_id": shoppinglist_objid
    }
    
    result = products_col.insert_one(products)
    print(f"Product {name} has been added!")
    
def list_products():
    # Find all the products from the database and print their information
    products = products_col.find()
    print("\nProducts:")
    for p in products:
        print("\nID:", p["_id"])
        print("Name:", p["name"])
        print("Brand:", p["brand"])
        print("Quantity:", p["quantity"])
        print("Tags:", p["tags"])
        print("Purchased:", p["isPurchased"])
        print("Shoppinglist ID:", p["shoppinglist_id"])
    
def edit_products():
    print("\nWhich product do you want to edit?")
    products_id = input("Product ID:")
    print("\nProvide the new information for the product")
    # Request new values for the product's fields from the user and update them based on the product's id

    try:
        products_objid = ObjectId(products_id)
    except:
        print("Invalid ID format")
        return
    
    pr = products_col.find_one({"_id": products_objid})
    
    name = input(f"\nNew name [{pr['name']}]: ") or pr['name']
    brand = input(f"New brand [{pr['brand']}]: ") or pr['brand']
    quantity = input(f"New quantity [{pr['quantity']}]: ") or pr['quantity']
    tags_input = input(f"New tags (comma separated) [{', '.join(pr['tags'])}]: ")
    tags = [t.strip() for t in tags_input.split(",")] if tags_input else pr['tags']
    isPurchased_input = input(f"Is purchased? (yes/no) [{pr['isPurchased']}]: ").strip().lower()
    isPurchased = pr['isPurchased'] 
    if isPurchased_input in ["yes", "y"]:
        isPurchased = True
    elif isPurchased_input in ["no", "n"]:
        isPurchased = False
    shoppinglists_id_input = input(f"New Shoppinglist ID [{pr['shoppinglist_id']}]: ").strip()
    if shoppinglists_id_input:
        try:
            shoppinglist_objid = ObjectId(shoppinglists_id_input)
        except:
            print("Invalid Shoppinglist ID format. Keeping old value.")
            shoppinglist_objid = pr['shoppinglist_id']
    else:
        shoppinglist_objid = pr['shoppinglist_id']
        
    # Päivitä dokumentti
    products_col.update_one(
        {"_id": products_objid},
        {"$set": {
            "name": name,
            "brand": brand,
            "quantity": quantity,
            "tags": tags,
            "isPurchased": isPurchased,
            "shoppinglist_id": shoppinglist_objid
        }}
    )

    print("Product updated.")
    
def delete_products():
    # Request product's id from the user and delete it
    print("\nWhich product do you want to delete?")
    products_id = input("Product's ID:")
    try:
        products_objid = ObjectId(products_id)
    except:
        print("Invalid ID format")
        return
    
    # Poista
    result = products_col.delete_one({"_id": products_objid})
    
    print(f"Product deleted.")


print_commands()

while True:
    command = input("\nType in the command number:")
    
    if command == "1":
        list_shoppinglists()
    elif command == "2":
        add_shoppinglists()
    elif command == "3":
        edit_shoppinglists()
    elif command == "4":
        delete_shoppinglists()  
    elif command == "5":
        list_products()
    elif command == "6":
        add_products()
    elif command == "7":
        edit_products()
    elif command == "8":
        delete_products()      
    elif command == "9":
        break
    else:
        print("I don't know that command")

print("Goodbye!")
