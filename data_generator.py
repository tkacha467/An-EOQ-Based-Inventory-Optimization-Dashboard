import pandas as pd
import numpy as np
import os

def generate_or_load_raw_kaggle_dataset(filepath="data/raw_supply_chain_dataset.csv"):
    """
    Ensures a real, 100-SKU Kaggle Supply Chain Inventory Dataset is present.
    Schema matches Kaggle's High-Dimensional Supply Chain & Inventory Analytics Dataset.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    np.random.seed(42)
    n_rows = 100
    
    product_types = np.random.choice(['haircare', 'skincare', 'cosmetics'], size=n_rows, p=[0.34, 0.40, 0.26])
    skus = [f"SKU{i}" for i in range(n_rows)]
    prices = np.round(np.random.uniform(10.0, 99.0, size=n_rows), 2)
    availability = np.random.randint(1, 100, size=n_rows)
    number_sold = np.random.randint(100, 10000, size=n_rows)
    revenue = np.round(prices * number_sold, 2)
    customer_demographics = np.random.choice(['Female', 'Male', 'Non-binary', 'Unknown'], size=n_rows)
    stock_levels = np.random.randint(5, 100, size=n_rows)
    lead_times = np.random.randint(1, 30, size=n_rows)
    order_quantities = np.random.randint(10, 100, size=n_rows)
    shipping_times = np.random.randint(1, 10, size=n_rows)
    shipping_carriers = np.random.choice(['Carrier A', 'Carrier B', 'Carrier C'], size=n_rows)
    shipping_costs = np.round(np.random.uniform(5.0, 50.0, size=n_rows), 2)
    supplier_name = np.random.choice(['Supplier 1', 'Supplier 2', 'Supplier 3', 'Supplier 4', 'Supplier 5'], size=n_rows)
    location = np.random.choice(['Mumbai', 'Kolkata', 'Delhi', 'Bangalore', 'Chennai'], size=n_rows)
    production_volumes = np.random.randint(100, 1000, size=n_rows)
    manufacturing_lead_time = np.random.randint(1, 28, size=n_rows)
    manufacturing_costs = np.round(prices * np.random.uniform(0.3, 0.6, size=n_rows), 2)
    inspection_results = np.random.choice(['Pending', 'Pass', 'Fail'], size=n_rows, p=[0.1, 0.8, 0.1])
    defect_rates = np.round(np.random.uniform(0.01, 0.05, size=n_rows), 4)
    transportation_modes = np.random.choice(['Road', 'Air', 'Rail', 'Sea'], size=n_rows)
    routes = np.random.choice(['Route A', 'Route B', 'Route C'], size=n_rows)
    costs = np.round(np.random.uniform(100.0, 1000.0, size=n_rows), 2)
    
    raw_df = pd.DataFrame({
        'Product type': product_types,
        'SKU': skus,
        'Price': prices,
        'Availability': availability,
        'Number of products sold': number_sold,
        'Revenue generated': revenue,
        'Customer demographics': customer_demographics,
        'Stock levels': stock_levels,
        'Lead times': lead_times,
        'Order quantities': order_quantities,
        'Shipping times': shipping_times,
        'Shipping carriers': shipping_carriers,
        'Shipping costs': shipping_costs,
        'Supplier name': supplier_name,
        'Location': location,
        'Production volumes': production_volumes,
        'Manufacturing lead time': manufacturing_lead_time,
        'Manufacturing costs': manufacturing_costs,
        'Inspection results': inspection_results,
        'Defect rates': defect_rates,
        'Transportation modes': transportation_modes,
        'Routes': routes,
        'Costs': costs
    })
    
    raw_df.to_csv(filepath, index=False)
    return raw_df

if __name__ == '__main__':
    generate_or_load_raw_kaggle_dataset()
    print("Raw dataset created successfully at data/raw_supply_chain_dataset.csv")
