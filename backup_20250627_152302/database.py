import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random

def create_sample_database():
    """Create sample database with sales and stock data"""
    conn = sqlite3.connect('business.db')
    
    # Create tables
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            date DATE,
            product_name TEXT,
            quantity INTEGER,
            price DECIMAL(10,2),
            total_amount DECIMAL(10,2)
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY,
            product_name TEXT,
            date DATE,
            movement_type TEXT,
            quantity INTEGER,
            current_stock INTEGER
        )
    ''')
    
    # Generate sample data
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones']
    
    # Sales data for last 2 months
    sales_data = []
    for i in range(100):
        date = datetime.now() - timedelta(days=random.randint(0, 60))
        product = random.choice(products)
        quantity = random.randint(1, 10)
        price = random.uniform(10, 1000)
        sales_data.append((date.date(), product, quantity, price, quantity * price))
    
    conn.executemany('INSERT INTO sales (date, product_name, quantity, price, total_amount) VALUES (?, ?, ?, ?, ?)', sales_data)
    
    # Stock movement data
    stock_data = []
    for i in range(50):
        date = datetime.now() - timedelta(days=random.randint(0, 30))
        product = random.choice(products)
        movement = random.choice(['IN', 'OUT'])
        quantity = random.randint(1, 20)
        current_stock = random.randint(10, 100)
        stock_data.append((product, date.date(), movement, quantity, current_stock))
    
    conn.executemany('INSERT INTO stock (product_name, date, movement_type, quantity, current_stock) VALUES (?, ?, ?, ?, ?)', stock_data)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_sample_database()
    print("Sample database created successfully!")