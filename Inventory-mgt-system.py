from datetime import datetime

inventory = [
    {"id" : 1, "item_name": "Laptop", "quantity" : 10, "price" : 899.99, "category" : "Electronics", "added_on" :"2025-05-19"},
    {"id" : 2, "item_name": "Chairs", "quantity" : 25, "price" : 120.50, "category" : "Furniture", "added_on" :"2025-05-10"},
    {"id" : 3, "item_name": "Books", "quantity" : 100, "price" : 3.99, "category" : "Stationery", "added_on" :"2025-05-20"}
]

def display_inventory(category_filter = None):
    """Display all items"""

    print("\nCurrent Inventory")
    print("-----------------------------------------------------------------------------------")
    print(f"{'ID':<5} {'Item':<15} {'Quantity':<10} {'Price':<10} {'Category':<15} {'Added on':<10}")
    print("-----------------------------------------------------------------------------------")
    for item in inventory:
        if category_filter is None or item["category"] == category_filter:
            print(f"{item['id']:<5} {item['item_name']:<15} {item['quantity']:<10} {item['price']:<9.2f} {item['category']:<15} {item['added_on']:<10}")

print()

def update_stock(item_id, quantity, action="add"):
    """Update stock quantity for an item."""

    for item in inventory:
        if item["id"] == item_id:
            if action == "add":
                item["quantity"] += quantity
                print(f"Added {quantity} units to {item['item_name']}. New quantity: {item['quantity']}")
            elif action == "remove":
                if item["quantity"] >= quantity:
                    item["quantity"] -= quantity
                    print(f"Removed {quantity} units from {item['item_name']}. New quantity: {item['quantity']}")

                    if item["quantity"] == 0:
                        print(f"Warning: {item['item_name']} is now out of stock.")
                else:
                    print(f"Cannot remove {quantity} units. Only {item['quantity']} available.")

def add_new_item(item_name, quantity, price, category):
    "Add a new item into the inventory"

    # Generate new id
    new_id = max(item["id"] for item in inventory) + 1

    #Get current date only
    added_on = datetime.now().strftime("%Y-%m-%d")

    new_item = {
        "id" : new_id,
        "item_name" : item_name,
        "quantity" : quantity,
        "price" : price,
        "category" : category,
        "added_on" : added_on
    }

    inventory.append(new_item)
    print(
        f"Added new item: {item_name} (ID: {new_id}, Quantity: {quantity}, Price: {price:.2f}, Category: {category}, Added on: {added_on})"
    )

def remove_item(item_id):
    "Remove an item from the Inventory Management System"

    for i, item in enumerate(inventory):
        if item["id"] == item_id:
            removed_item = inventory.pop()
            print(f"Removed item : {removed_item['item_name']}")

def get_categories():
    "Return a list of unique categories"
    return sorted(set(item["category"] for item in inventory))

while True:
    print("\nInventory Management System")
    print("1. Display All Inventory")
    print("2. Display by category")
    print("3. Add Stock")
    print("4. Remove Stock")
    print("5. Add new Item")
    print("6. Remove an Item")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        display_inventory()

    elif choice == "2":
        categories = get_categories()
        print("\nAvaiable Categories", ", ".join(categories))

        category = input("Enter category to filter: ").capitalize()
        if category and category not in categories:
            print(f"Category {category} not found!")
        else:
            display_inventory(category if category else None)

    elif choice == "3":
        try:
            item_id = int(input("Enter item ID: "))
            quantity = int(input("Enter the quantity to add: "))

            if quantity < 0:
                print("Error: Quantity cannot be negative")
            else:
                update_stock(item_id, quantity, "add")

        except ValueError:
            print("Please enter valid numbers for ID and quantity")

    elif choice == "4":

        try:
            item_id = int(input("Enter item ID: "))
            quantity = int(input("Enter the quantity to remove: "))

            if quantity < 0:
                print("Quantity cannot be negative")
            else:
                update_stock(item_id, quantity, "remove")
                
        except ValueError:
            print("Please enter valid numbers for ID and quantity")

        
    elif choice == "5":
        item_name = input("Enter item name: ")

        try:
            quantity = int(input("Enter initial quantity: "))
            price = float(input("Enter the price: "))
            category = input("Enter the category: ").capitalize()

            if quantity < 0 or price < 0:
                print("Quantity and Price cannot be less than zero")
            else:
                add_new_item(item_name, quantity, price, category)

        except ValueError:
            print("Please enter valid numbers for quantity or price!")

    elif choice == "6":
        try:
            item_id = int(input("Enter the item id: "))
            remove_item(item_id)
        except ValueError:
            print("Enter a valid ID number")


    elif choice == "7":
        print("Exiting Inventory Management System. Thanks?")
        break

    else:
        print("Invalid choice. Please select 1-7")
