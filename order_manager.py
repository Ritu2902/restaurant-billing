import os
import time

class OrderManager:
    def __init__(self, data_file="data/orders.txt"):
        self.data_file = data_file
        self.orders = {} 
        self.next_order_id = 1
        self.load_orders()
    
    def load_orders(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.strip():
                            parts = line.strip().split('|')
                            if len(parts) == 6:
                                order_id = int(parts[0])
                                table = parts[1]
                                items_str = parts[2]
                                items = []
                                if items_str:
                                    for item_str in items_str.split(';'):
                                        if item_str:
                                            item_parts = item_str.split(',')
                                            if len(item_parts) == 3:
                                                items.append([item_parts[0], float(item_parts[1]), int(item_parts[2])])
                                status = parts[3]
                                total = float(parts[4])
                                timestamp = parts[5]
                                
                                self.orders[order_id] = [table, items, status, total, timestamp]
                                
                                if order_id >= self.next_order_id:
                                    self.next_order_id = order_id + 1
            except Exception as e:
                print(f"Error loading orders: {e}")
                self.orders = {}
        else:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            self.save_orders()
    
    def save_orders(self):
        try:
            with open(self.data_file, 'w') as f:
                for order_id, order_data in self.orders.items():
                    table, items, status, total, timestamp = order_data
                    
                    items_str = ';'.join([f"{item[0]},{item[1]},{item[2]}" for item in items])
                    
                    line = f"{order_id}|{table}|{items_str}|{status}|{total}|{timestamp}\n"
                    f.write(line)
        except Exception as e:
            print(f"Error saving orders: {e}")
    
    def create_order(self, table_number):
        order_id = self.next_order_id
        self.next_order_id += 1
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.orders[order_id] = [table_number, [], "active", 0.0, timestamp]
        self.save_orders()
        
        return order_id
    
    def get_order(self, order_id):
        return self.orders.get(order_id)
    
    def add_item_to_order(self, order_id, item_name, price, quantity=1):
        if order_id not in self.orders:
            return False, "Order not found!"
        
        table, items, status, total, timestamp = self.orders[order_id]
        
        if status != "active":
            return False, "Order is not active!"
        
        for i, item in enumerate(items):
            if item[0].lower() == item_name.lower():
                items[i][2] += quantity
                self.save_orders()
                return True, f"Added {quantity} more {item_name}(s)"
        
        items.append([item_name, price, quantity])
        self.save_orders()
        return True, f"Added {item_name} x{quantity}"
    
    def remove_item_from_order(self, order_id, item_index):
        if order_id not in self.orders:
            return False, "Order not found!"
        
        table, items, status, total, timestamp = self.orders[order_id]
        
        if status != "active":
            return False, "Order is not active!"
        
        if 0 <= item_index < len(items):
            item_name = items[item_index][0]
            del items[item_index]
            self.save_orders()
            return True, f"Removed {item_name} from order"
        
        return False, "Item not found!"
    
    def update_item_quantity(self, order_id, item_index, quantity):
        if order_id not in self.orders:
            return False, "Order not found!"
        
        table, items, status, total, timestamp = self.orders[order_id]
        
        if status != "active":
            return False, "Order is not active!"
        
        if 0 <= item_index < len(items):
            if quantity <= 0:
                item_name = items[item_index][0]
                del items[item_index]
                self.save_orders()
                return True, f"Removed {item_name} from order"
            
            items[item_index][2] = quantity
            self.save_orders()
            return True, f"Updated quantity to {quantity}"
        
        return False, "Item not found!"
    
    def calculate_total(self, items):
        subtotal = sum(item[1] * item[2] for item in items)
        tax = subtotal * 0.05
        total = subtotal + tax
        return subtotal, tax, total
    
    def complete_order(self, order_id):
        if order_id not in self.orders:
            return False, "Order not found!"
        
        table, items, status, total, timestamp = self.orders[order_id]
        
        if status != "active":
            return False, "Order is not active!"
        
        if not items:
            return False, "Cannot complete empty order!"
        
        _, _, total = self.calculate_total(items)
        self.orders[order_id] = [table, items, "completed", total, timestamp]
        self.save_orders()
        return True, f"Order #{order_id} completed! Total: ₹{total:.2f}"
    
    def cancel_order(self, order_id):
        if order_id not in self.orders:
            return False, "Order not found!"
        
        table, items, status, total, timestamp = self.orders[order_id]
        self.orders[order_id] = [table, items, "cancelled", 0.0, timestamp]
        self.save_orders()
        return True, f"Order #{order_id} cancelled!"
    
    def get_active_orders(self):
        active = {}
        for order_id, order_data in self.orders.items():
            if order_data[2] == "active":
                active[order_id] = order_data
        return active
    
    def get_order_history(self):
        history = {}
        for order_id, order_data in self.orders.items():
            if order_data[2] == "completed":
                history[order_id] = order_data
        return history
    
    def get_todays_orders(self):
        today = time.strftime("%Y-%m-%d")
        todays = {}
        for order_id, order_data in self.orders.items():
            timestamp = order_data[4]
            if timestamp.startswith(today):
                todays[order_id] = order_data
        return todays
    
    def get_daily_revenue(self):
        todays_orders = self.get_todays_orders()
        revenue = 0
        for order_id, order_data in todays_orders.items():
            if order_data[2] == "completed":
                revenue += order_data[3]
        return revenue
    
    def get_most_ordered_items(self, limit=5):
        item_counts = {}
        for order_id, order_data in self.orders.items():
            if order_data[2] == "completed":
                items = order_data[1]
                for item in items:
                    name = item[0]
                    quantity = item[2]
                    if name in item_counts:
                        item_counts[name] += quantity
                    else:
                        item_counts[name] = quantity
        
        sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:limit]