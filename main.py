from menu_manager import MenuManager
from order_manager import OrderManager
from bill_generator import BillGenerator
from utils import *
import time

def main():
    menu_manager = MenuManager()
    order_manager = OrderManager()
    bill_generator = BillGenerator()
    
    while True:
        clear_screen()
        show_main_menu()
        choice = get_user_input("Select an option (1-14)")
        
        if choice == "1":
            clear_screen()
            print_header("VIEW MENU")
            
            categories = menu_manager.get_categories()
            print("Categories:", ", ".join(categories))
            print("\nAll Items:\n")
            items = menu_manager.get_available_items()
            print_menu_items(items)
            input("Press Enter to continue...")
        
        elif choice == "2":
            clear_screen()
            print_header("ADD MENU ITEM")
            
            name = get_user_input("Item name")
            if not name:
                print("Name is required!")
                input("Press Enter to continue...")
                continue
            
            category = get_user_input("Category (Appetizer/Main Course/Dessert/Beverage)")
            price = get_number_input("Price (₹): ", min_val=0)
            description = get_user_input("Description (optional)")
            
            success, message = menu_manager.add_item(name, category, price, description)
            print(f"\n {message}")
            input("Press Enter to continue...")
        
        elif choice == "3":
            clear_screen()
            print_header("UPDATE MENU ITEM")
            items = menu_manager.get_all_items()
            print_menu_items(items)
            
            try:
                index = int(get_user_input("Enter item number to update")) - 1
                if 0 <= index < len(items):
                    item = items[index]
                    print(f"\nCurrent details for {item[0]}:")
                    print(f"  Category: {item[1]}")
                    print(f"  Price: ₹{item[2]:.2f}")
                    print(f"  Description: {item[3]}")
                    print(f"  Available: {'Yes' if item[4] else 'No'}")
                    print("\n(Leave blank to keep current value)\n")
                    
                    name = get_user_input("New name", item[0])
                    category = get_user_input("New category", item[1])
                    price_str = get_user_input("New price", str(item[2]))
                    price = float(price_str) if price_str else item[2]
                    description = get_user_input("New description", item[3])
                    available_str = get_user_input("Available? (y/n)", "y" if item[4] else "n")
                    available = available_str.lower() == 'y' if available_str else item[4]
                    
                    success, message = menu_manager.update_item(
                        index, name, category, price, description, available
                    )
                    print(f"\n {message}")
                else:
                    print(" Invalid item number!")
            except ValueError:
                print(" Please enter a valid number!")
            
            input("Press Enter to continue...")
        
        elif choice == "4":
            # Remove Menu Item
            clear_screen()
            print_header("REMOVE MENU ITEM")
            items = menu_manager.get_all_items()
            print_menu_items(items)
            
            try:
                index = int(get_user_input("Enter item number to remove")) - 1
                if 0 <= index < len(items):
                    name = items[index][0]
                    confirm = input(f"Are you sure you want to remove '{name}'? (y/n): ").lower()
                    if confirm == 'y':
                        success, message = menu_manager.remove_item(index)
                        print(f"\n {message}")
                    else:
                        print(" Operation cancelled")
                else:
                    print(" Invalid item number!")
            except ValueError:
                print(" Please enter a valid number!")
            
            input("Press Enter to continue...")
        
        elif choice == "5":
            clear_screen()
            print_header("CREATE NEW ORDER")
            
            table_number = get_user_input("Table number")
            if not table_number:
                print(" Table number is required!")
                input("Press Enter to continue...")
                continue
            
            order_id = order_manager.create_order(table_number)
            print(f"\n Order #{order_id} created for Table {table_number}!")
            input("Press Enter to continue...")
        
        elif choice == "6":
            clear_screen()
            print_header("ACTIVE ORDERS")
            active_orders = order_manager.get_active_orders()
            
            if not active_orders:
                print("No active orders!")
            else:
                for order_id, order_data in active_orders.items():
                    table, items, status, total, timestamp = order_data
                    print(f"Order #{order_id} | Table {table} | Items: {len(items)}")
                    if items:
                        print("  Items:")
                        for item in items:
                            print(f"    {item[0]} x{item[2]} = ₹{item[1] * item[2]:.2f}")
                    print("-"*40)
            
            input("Press Enter to continue...")
        
        elif choice == "7":
            clear_screen()
            print_header("ADD ITEM TO ORDER")
            
            active_orders = order_manager.get_active_orders()
            if not active_orders:
                print("No active orders! Create one first.")
                input("Press Enter to continue...")
                continue
            
            print("Active Orders:")
            order_list = list(active_orders.keys())
            for i, order_id in enumerate(order_list, 1):
                table, items, status, total, timestamp = active_orders[order_id]
                print(f"{i}. Order #{order_id} | Table {table} | Items: {len(items)}")
            
            try:
                choice_num = int(get_user_input("\nSelect order number")) - 1
                if 0 <= choice_num < len(order_list):
                    order_id = order_list[choice_num]
                else:
                    print(" Invalid selection!")
                    input("Press Enter to continue...")
                    continue
            except ValueError:
                print(" Please enter a valid number!")
                input("Press Enter to continue...")
                continue
            
            print("\nAvailable Menu Items:")
            items = menu_manager.get_available_items()
            print_menu_items(items)
            
            try:
                item_choice = int(get_user_input("Select item number")) - 1
                if 0 <= item_choice < len(items):
                    item = items[item_choice]
                    quantity = int(get_number_input("Quantity: ", min_val=1))
                    
                    success, message = order_manager.add_item_to_order(
                        order_id, item[0], item[2], quantity
                    )
                    print(f"\n {message}")
                else:
                    print(" Invalid item number!")
            except ValueError:
                print(" Please enter a valid number!")
            
            input("Press Enter to continue...")
        
        elif choice == "8":
            clear_screen()
            print_header("COMPLETE ORDER & BILL")
            
            active_orders = order_manager.get_active_orders()
            if not active_orders:
                print("No active orders to complete!")
                input("Press Enter to continue...")
                continue
            
            print("Active Orders:")
            order_list = list(active_orders.keys())
            for i, order_id in enumerate(order_list, 1):
                table, items, status, total, timestamp = active_orders[order_id]
                print(f"{i}. Order #{order_id} | Table {table} | Items: {len(items)}")
            
            try:
                choice_num = int(get_user_input("\nSelect order number")) - 1
                if 0 <= choice_num < len(order_list):
                    order_id = order_list[choice_num]
                    order_data = active_orders[order_id]
                else:
                    print(" Invalid selection!")
                    input("Press Enter to continue...")
                    continue
            except ValueError:
                print(" Please enter a valid number!")
                input("Press Enter to continue...")
                continue
            
            if not order_data[1]: 
                print(" Cannot complete empty order!")
                input("Press Enter to continue...")
                continue
            
            print_order_summary(order_id, order_data)
            
            confirm = input("Complete this order and generate bill? (y/n): ").lower()
            if confirm != 'y':
                print(" Operation cancelled")
                input("Press Enter to continue...")
                continue
            
            success, message = order_manager.complete_order(order_id)
            if success:
                print(f" {message}")
                updated_order = order_manager.get_order(order_id)
                if updated_order:
                    bill_generator.print_receipt(order_id, updated_order)
            else:
                print(f" {message}")
            
            input("Press Enter to continue...")
        
        elif choice == "9":
            clear_screen()
            print_header("CANCEL ORDER")
            
            active_orders = order_manager.get_active_orders()
            if not active_orders:
                print("No active orders to cancel!")
                input("Press Enter to continue...")
                continue
            
            print("Active Orders:")
            order_list = list(active_orders.keys())
            for i, order_id in enumerate(order_list, 1):
                table, items, status, total, timestamp = active_orders[order_id]
                print(f"{i}. Order #{order_id} | Table {table} | Items: {len(items)}")
            
            try:
                choice_num = int(get_user_input("\nSelect order number")) - 1
                if 0 <= choice_num < len(order_list):
                    order_id = order_list[choice_num]
                else:
                    print("Invalid selection!")
                    input("Press Enter to continue...")
                    continue
            except ValueError:
                print("Please enter a valid number!")
                input("Press Enter to continue...")
                continue
            
            confirm = input(f"Are you sure you want to cancel Order #{order_id}? (y/n): ").lower()
            if confirm == 'y':
                success, message = order_manager.cancel_order(order_id)
                print(f"\n{message}")
            else:
                print(" Operation cancelled")
            input("Press Enter to continue...")
        
        elif choice == "10":
            clear_screen()
            print_header("DAILY REVENUE")
            revenue = order_manager.get_daily_revenue()
            todays_orders = order_manager.get_todays_orders()
            
            print(f"Date: {time.strftime('%Y-%m-%d')}")
            print(f"Total Orders Today: {len(todays_orders)}")
            
            completed = 0
            for order_id, order_data in todays_orders.items():
                if order_data[2] == "completed":
                    completed += 1
            
            print(f"Completed Orders: {completed}")
            print(f"Total Revenue: ₹{revenue:.2f}")
            
            if todays_orders:
                print("\nToday's Orders:")
                for order_id, order_data in todays_orders.items():
                    table, items, status, total, timestamp = order_data
                    status_display = "✓" if status == "completed" else "⏳"
                    print(f"  {status_display} Order #{order_id} | Table {table} | {status} | ₹{total:.2f}")
            
            input("Press Enter to continue...")
        
        elif choice == "11":
            clear_screen()
            print_header("MOST POPULAR ITEMS")
            popular = order_manager.get_most_ordered_items(5)
            
            if popular:
                print("Top 5 Most Ordered Items:")
                print("-"*40)
                for i, (name, count) in enumerate(popular, 1):
                    print(f"{i}. {name}: {count} orders")
            else:
                print("No orders completed yet!")
            
            input("Press Enter to continue...")
        
        elif choice == "12":
            clear_screen()
            print_header("ORDER HISTORY")
            history = order_manager.get_order_history()
            
            if not history:
                print("No completed orders yet!")
            else:
                for order_id, order_data in history.items():
                    table, items, status, total, timestamp = order_data
                    print(f"Order #{order_id} | Table {table} | ₹{total:.2f} | {timestamp}")
                    for item in items:
                        print(f"  {item[0]} x{item[2]} = ₹{item[1] * item[2]:.2f}")
                    print("-"*40)
            
            input("Press Enter to continue...")
        
        elif choice == "13":
            clear_screen()
            print_header("SEARCH MENU")
            search_term = get_user_input("Enter search term (name, category, or description)")
            if search_term:
                results = menu_manager.search_items(search_term)
                if results:
                    print_menu_items(results, f"Results for '{search_term}'")
                else:
                    print(f" No results found for '{search_term}'")
            input("Press Enter to continue...")
        
        elif choice == "14":
      
            clear_screen()
            print_header("THANK YOU!")
            print(" All data has been saved.")
            print("Come back soon! \n")
            break
        
        else:
            print(" Invalid option! Please select 1-14")
            input("Press Enter to continue...")

if __name__ == "__main__":
    clear_screen()
    print(" Welcome to Restaurant Billing System! ")
    print("Your complete restaurant management solution\n")
    input("Press Enter to start...")
    clear_screen()
    main()