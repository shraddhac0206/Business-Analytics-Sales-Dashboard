"""
Script to generate a sample sales dataset for the business analytics dashboard.
Run this once to create the sales_data.csv file.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate date range (last 12 months)
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
dates = pd.date_range(start_date, end_date, freq='D')

# Define categories, regions, and customer names
categories = ['Electronics', 'Clothing', 'Food & Beverages', 'Home & Garden', 'Sports & Outdoors']
regions = ['North', 'South', 'East', 'West', 'Central']
customers = [f'Customer_{i:03d}' for i in range(1, 51)]  # 50 customers

# Generate sample data
n_records = 5000
data = []

for _ in range(n_records):
    date = np.random.choice(dates)
    category = np.random.choice(categories)
    region = np.random.choice(regions)
    customer = np.random.choice(customers)
    
    # Generate sales amount (with some variation by category)
    base_sales = {
        'Electronics': 500,
        'Clothing': 150,
        'Food & Beverages': 80,
        'Home & Garden': 200,
        'Sports & Outdoors': 180
    }
    
    sales_amount = np.random.normal(base_sales[category], base_sales[category] * 0.5)
    sales_amount = max(10, sales_amount)  # Minimum $10
    
    # Cost is typically 60-70% of sales (30-40% margin)
    cost = sales_amount * np.random.uniform(0.6, 0.7)
    
    # Profit = Sales - Cost
    profit = sales_amount - cost
    
    # Margin = (Profit / Sales) * 100
    margin = (profit / sales_amount) * 100
    
    data.append({
        'date': date,
        'product_category': category,
        'region': region,
        'customer': customer,
        'sales_amount': round(sales_amount, 2),
        'cost': round(cost, 2),
        'profit': round(profit, 2),
        'margin': round(margin, 2)
    })

# Create DataFrame
df = pd.DataFrame(data)

# Sort by date
df = df.sort_values('date').reset_index(drop=True)

# Save to CSV
df.to_csv('sales_data.csv', index=False)
print(f"Generated {len(df)} sales records")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"\nSample data:")
print(df.head(10))
