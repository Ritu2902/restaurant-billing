import os

class MenuManager:
    def __init__(self, data_file="data/menu.txt"):
        self.data_file = data_file
        self.menu_items = []  
        self.load_menu()
    
    def load_menu(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.strip():
                            # Format: name|category|price|description|available
                            parts = line.strip().split('|')
                            if len(parts) == 5:
                                name = parts[0]
                                category = parts[1]
                                price = float(parts[2])
                                description = parts[3]
                                available = parts[4].lower() == 'true'
                                self.menu_items.append([name, category, price, description, available])
            except Exception:
                self.menu_items = []
                self.add_sample_items()
        else:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            self.add_sample_items()
    
    def save_menu(self):
        with open(self.data_file, 'w') as f:
            for item in self.menu_items:
                line = f"{item[0]}|{item[1]}|{item[2]}|{item[3]}|{item[4]}\n"
                f.write(line)
    
    def add_sample_items(self):
        self.menu_items = [
            ["Margherita Pizza", "Main Course", 250, "Classic cheese and tomato pizza", True],
            ["Chicken Tikka", "Appetizer", 180, "Grilled chicken in special spices", True],
            ["Biryani", "Main Course", 320, "Fragrant rice with meat and spices", True],
            ["Garlic Bread", "Appetizer", 120, "Toasted bread with garlic butter", True],
            ["Cold Coffee", "Beverage", 80, "Cold coffee with ice cream", True],
            ["Chocolate Brownie", "Dessert", 150, "Warm brownie with ice cream", True],
            ["Pasta Alfredo", "Main Course", 280, "Creamy pasta with parmesan", True],
            ["Mango Lassi", "Beverage", 90, "Sweet mango yogurt drink", True],
            ["Spring Rolls", "Appetizer", 160, "Crispy vegetable rolls", True],
            ["Gulab Jamun", "Dessert", 130, "Sweet milk balls in sugar syrup", True],
        ]
        self.save_menu()
    
    def get_categories(self):
        categories = set()
        for item in self.menu_items:
            categories.add(item[1])
        return sorted(list(categories))
    
    def add_item(self, name, category, price, description=""):
        for item in self.menu_items:
            if item[0].lower() == name.lower():
                return False, "Item already exists!"
        
        self.menu_items.append([name, category, price, description, True])
        self.save_menu()
        return True, f"Added {name} to menu!"
    
    def remove_item(self, index):
        if 0 <= index < len(self.menu_items):
            name = self.menu_items[index][0]
            del self.menu_items[index]
            self.save_menu()
            return True, f"Removed {name} from menu!"
        return False, "Item not found!"
    
    def update_item(self, index, name=None, category=None, price=None, description=None, available=None):
        if 0 <= index < len(self.menu_items):
            if name:
                self.menu_items[index][0] = name
            if category:
                self.menu_items[index][1] = category
            if price is not None:
                self.menu_items[index][2] = price
            if description is not None:
                self.menu_items[index][3] = description
            if available is not None:
                self.menu_items[index][4] = available
            
            self.save_menu()
            return True, "Item updated successfully!"
        return False, "Item not found!"
    
    def get_available_items(self):
        return [item for item in self.menu_items if item[4]]
    
    def get_all_items(self):
        return self.menu_items
    
    def search_items(self, search_term):
        search_term = search_term.lower()
        results = []
        for item in self.menu_items:
            if search_term in item[0].lower() or search_term in item[1].lower() or search_term in item[3].lower():
                results.append(item)
        return results
    
    def get_item_by_index(self, index):
        if 0 <= index < len(self.menu_items):
            return self.menu_items[index]
        return None