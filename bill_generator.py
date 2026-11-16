import os
import time

class BillGenerator:
    def __init__(self, receipt_dir="receipts"):
        self.receipt_dir = receipt_dir
        if not os.path.exists(receipt_dir):
            os.makedirs(receipt_dir)
    
    def generate_receipt(self, order_id, order_data):
        table, items, status, total, timestamp = order_data
        
        if status != "completed":
            return None, "Order is not completed!"
        
        subtotal = sum(item[1] * item[2] for item in items)
        tax = subtotal * 0.05
        grand_total = subtotal + tax
        
        receipt_lines = []
        receipt_lines.append("="*60)
        receipt_lines.append("     RESTAURANT BILL     ".center(60))
        receipt_lines.append("="*60)
        receipt_lines.append(f"Order #: {order_id}")
        receipt_lines.append(f"Table: {table}")
        receipt_lines.append(f"Date: {timestamp}")
        receipt_lines.append("-"*60)
        receipt_lines.append(f"{'Item':<30} {'Qty':>8} {'Price':>10} {'Total':>10}")
        receipt_lines.append("-"*60)
        
        for item in items:
            name, price, quantity = item
            item_total = price * quantity
            receipt_lines.append(f"{name[:28]:<30} {quantity:>8} Rs.{price:>8.2f} Rs.{item_total:>8.2f}")
        
        receipt_lines.append("-"*60)
        receipt_lines.append(f"{'Subtotal':>48} Rs.{subtotal:>10.2f}")
        receipt_lines.append(f"{'GST (5%)':>48} Rs.{tax:>10.2f}")
        receipt_lines.append("="*60)
        receipt_lines.append(f"{'TOTAL':>48} Rs.{grand_total:>10.2f}")
        receipt_lines.append("="*60)
        receipt_lines.append("     Thank you for dining with us!     ".center(60))
        receipt_lines.append("     Please visit again!     ".center(60))
        receipt_lines.append("="*60)
        
        receipt_text = "\n".join(receipt_lines)
        
        filename = f"receipt_{order_id}_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(self.receipt_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(receipt_text)
        
        return receipt_text, filepath
    
    def print_receipt(self, order_id, order_data):
        """Print receipt to console and save to file"""
        receipt_text, filepath = self.generate_receipt(order_id, order_data)
        if receipt_text:
            print("\n" + receipt_text + "\n")
            print(f"Receipt saved to: {filepath}")
        return receipt_text