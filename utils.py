import os
import platform

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def print_header(title):
    print("\n" + "="*60)
    print(f" {title} ".center(60, "="))
    print("="*60 + "\n")

def print_menu_items(items, title="Menu Items"):
    if not items:
        print("No items to display.\n")
        return
    
    print(f"\n{title}:")
    print("-"*70)
    print(f"{'#':<4} {'Name':<25} {'Category':<15} {'Price':<10} {'Status':<10}")
    print("-"*70)
    
    for i, item in enumerate(items, 1):
        status = "✓ Available" if item[4] else "✗ Unavailable"
        print(f"{i:<4} {item[0][:24]:<25} {item[1][:14]:<15} ₹{item[2]:<8.2f} {status:<10}")
    
    print("-"*70 + "\n")

def print_order_summary(order_id, order_data):
    if not order_data:
        print("No order to display.")
        return
    
    table, items, status, total, timestamp = order_data
    
    print(f"\nOrder #{order_id} | Table {table} | Status: {status.upper()}")
    print("-"*60)
    print(f"{'Item':<30} {'Qty':>8} {'Price':>10} {'Total':>10}")
    print("-"*60)
    
    subtotal = 0
    for item in items:
        name, price, quantity = item
        item_total = price * quantity
        subtotal += item_total
        print(f"{name[:28]:<30} {quantity:>8} ₹{price:>8.2f} ₹{item_total:>8.2f}")
    
    tax = subtotal * 0.05
    grand_total = subtotal + tax
    
    print("-"*60)
    print(f"{'Subtotal':>48} ₹{subtotal:>10.2f}")
    print(f"{'GST (5%)':>48} ₹{tax:>10.2f}")
    print("="*60)
    print(f"{'TOTAL':>48} ₹{grand_total:>10.2f}")
    print("="*60 + "\n")

def get_user_input(prompt, default=None):
    if default is not None:
        user_input = input(f"{prompt} (default: {default}): ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()

def get_number_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f" Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f" Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print(" Please enter a valid number!")

def show_main_menu():
    """Display the main menu"""
    print_header("RESTAURANT BILLING SYSTEM")
    print("1.  View Menu")
    print("2.  Add Menu Item")
    print("3.  Update Menu Item")
    print("4.  Remove Menu Item")
    print("5.  Create New Order")
    print("6.  View Active Orders")
    print("7.  Add Item to Order")
    print("8.  Complete Order & Generate Bill")
    print("9.  Cancel Order")
    print("10.  View Daily Revenue")
    print("11.  View Popular Items")
    print("12.  View Order History")
    print("13.  Search Menu")
    print("14.  Exit")
    print("\n" + "-"*60)