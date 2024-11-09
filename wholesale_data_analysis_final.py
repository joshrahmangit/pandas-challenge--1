
# Import necessary libraries
import pandas as pd

# Load the dataset
data = pd.read_csv('/path/to/your/client_dataset.csv')

# View column names
print("Column Names:", data.columns)

# Generate summary statistics for numerical columns
data_description = data.describe()
print("Data Description:\n", data_description)

# Identify the category with the most entries
top_category = data['category'].value_counts().idxmax()
print("Category with the most entries:", top_category)

# Identify the subcategory with the most entries within the top category
top_subcategory = data[data['category'] == top_category]['subcategory'].value_counts().idxmax()
print("Top subcategory in the category '{}': {}".format(top_category, top_subcategory))

# Identify the top 5 clients with the most entries and store their IDs in a list
top_clients = data['client_id'].value_counts().head(5)
top_client_ids = top_clients.index.tolist()
print("Top 5 clients with the most entries:", top_client_ids)

# Calculate the total units ordered by the client with the most entries
total_units_top_client = data[data['client_id'] == top_client_ids[0]]['qty'].sum()
print("Total units ordered by the client with the most entries (ID={}): {}".format(top_client_ids[0], total_units_top_client))

# Create a 'subtotal' column
data['subtotal'] = data['unit_price'] * data['qty']

# Create a 'shipping_price' column with conditional pricing
data['shipping_price'] = data['unit_weight'].apply(lambda x: 7 if x > 50 else 10) * data['unit_weight']

# Create a 'total_price' column including sales tax of 9.25%
data['total_price'] = (data['subtotal'] + data['shipping_price']) * 1.0925

# Create a 'line_cost' column using unit cost, qty, and shipping price
data['line_cost'] = (data['unit_cost'] * data['qty']) + data['shipping_price']

# Create a 'profit' column by subtracting line cost from total price
data['profit'] = data['total_price'] - data['line_cost']

# Verify the total prices for specified Order IDs
order_ids_to_check = [2742071, 2173913, 6128929]
expected_totals = {
    2742071: 152811.89,
    2173913: 162388.71,
    6128929: 923441.25
}
actual_totals = {order_id: data[data['order_id'] == order_id]['total_price'].sum() for order_id in order_ids_to_check}
for order_id, expected in expected_totals.items():
    actual = actual_totals[order_id]
    print(f"Order ID {order_id}: Expected = {expected}, Actual = {actual}")

# Calculate total revenue for each of the top 5 clients
client_revenue = {client_id: data[data['client_id'] == client_id]['total_price'].sum() for client_id in top_client_ids}
print("Total revenue for top 5 clients:", client_revenue)

# Create a summary DataFrame for the top 5 clients
summary_data = []
for client_id in top_client_ids:
    client_data = data[data['client_id'] == client_id]
    total_units = client_data['qty'].sum()
    total_shipping = client_data['shipping_price'].sum()
    total_revenue = client_data['total_price'].sum()
    total_profit = client_data['profit'].sum()
    summary_data.append([client_id, total_units, total_shipping, total_revenue, total_profit])
summary_df = pd.DataFrame(summary_data, columns=['Client ID', 'Total Units Purchased', 'Total Shipping Price', 'Total Revenue', 'Total Profit'])

# Function to format values in millions
def format_to_millions(value):
    return round(value / 1_000_000, 2)

# Format relevant columns to millions and rename for presentation
summary_df['Total Units (M)'] = summary_df['Total Units Purchased'].apply(format_to_millions)
summary_df['Total Shipping (M)'] = summary_df['Total Shipping Price'].apply(format_to_millions)
summary_df['Total Revenue (M)'] = summary_df['Total Revenue'].apply(format_to_millions)
summary_df['Total Profit (M)'] = summary_df['Total Profit'].apply(format_to_millions)

# Final formatted summary DataFrame with sorting by 'Total Profit (M)'
formatted_summary_df = summary_df[['Client ID', 'Total Units (M)', 'Total Shipping (M)', 'Total Revenue (M)', 'Total Profit (M)']]
formatted_summary_df = formatted_summary_df.sort_values(by='Total Profit (M)', ascending=False)
print("Formatted Summary DataFrame:\n", formatted_summary_df)

# Summary of Findings
summary_text = '''
The analysis of the top 5 clients by quantity reveals that Client ID 24741 is the highest contributor to total revenue and profit, with significantly higher spending and profit generation compared to the other clients.
While all top clients contribute meaningfully, Client ID 24741’s revenue and profit figures stand out, indicating a particularly valuable customer relationship. 
The data suggests that focusing on similar high-volume, high-profit clients could be beneficial for maximizing profitability.
'''
print(summary_text)
