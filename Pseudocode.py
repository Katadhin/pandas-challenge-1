import pandas as pd

# Part 1: Explore the Data
# Import the data from the CSV file
df = pd.read_csv('Resources/client_dataset.csv')

# View the column names
column_names = df.columns

# Basic statistics of numerical columns
data_description = df.describe()

# Identify the top three item categories with the most entries
top_categories = df['category'].value_counts().head(3)

# Identify the subcategory with the most entries in the top category
most_entries_category = top_categories.index[0]
subcategory_most_entries = df[df['category'] == most_entries_category]['subcategory'].value_counts().index[0]

# Identify the top 5 clients with the most entries in the data
top_clients = df['client_id'].value_counts().head(5).index.tolist()

# Find out how many total units the client with the most entries ordered
client_with_most_entries = top_clients[0]
total_units_ordered = df[df['client_id'] == client_with_most_entries]['qty'].sum()

# Part 2: Transform the Data
# Create a column that calculates the subtotal for each line
df['subtotal'] = df['unit_cost'] * df['qty']

# Create a column for shipping price based on your criteria
df['shipping_price'] = df['qty'] * 0.05

# Create a column for the total price including sales tax
df['total_price'] = df['subtotal'] + df['shipping_price'] * 1.075

# Create a column for the cost of each line
df['line_cost'] = df['unit_cost'] * df['qty']

# Create a column for the profit of each line
df['line_profit'] = df['total_price'] - df['line_cost']

# Part 3: Confirm Your Work
# Check if the calculated total prices match the given Order IDs
order_checks = {
    'Order ID 2742071': 152811.89,
    'Order ID 2173913': 162388.71,
    'Order ID 6128929': 923441.25
}

for order_id, expected_price in order_checks.items():
    calculated_price = df[df['order_id'] == int(order_id.split()[-1])]['total_price'].sum()
    print(f'{order_id} - Calculated Price: ${calculated_price:.2f}, Expected Price: ${expected_price:.2f}')

# Part 4: Summarize and Analyze
# Calculate total revenue from each of the top 5 clients
client_revenues = df[df['client_id'].isin(top_clients)].groupby('client_id')['total_price'].sum()

# Create a summary DataFrame
summary_df = pd.DataFrame({
    'Total Units Purchased (Millions)': df[df['client_id'].isin(top_clients)].groupby('client_id')['qty'].sum() / 1_000_000,
    'Total Shipping Price (Millions)': df[df['client_id'].isin(top_clients)].groupby('client_id')['shipping_price'].sum() / 1_000_000,
    'Total Revenue (Millions)': client_revenues / 1_000_000,
    'Total Profit (Millions)': df[df['client_id'].isin(top_clients)].groupby('client_id')['line_profit'].sum() / 1_000_000
})

# Sort the summary DataFrame by total profit
summary_df = summary_df.sort_values(by='Total Profit (Millions)', ascending=False)

# Print the final summary DataFrame and total units ordered by the top client
print(column_names)
print(data_description)
print(top_categories)
print(most_entries_category)
print(subcategory_most_entries)
print(top_clients)
print(f'Total Units Ordered by Top Client ({client_with_most_entries}): {total_units_ordered}')
print(summary_df)

# Brief summary of findings
summary_text = f"In this analysis, we identified the top clients in terms of quantity, calculated shipping costs, and derived revenue and profit. The top client with the most entries ordered a total of {total_units_ordered} units."
print(summary_text)
