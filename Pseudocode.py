import pandas as pd

# Part 1: Explore the Data
# Import the data from the CSV file
df = pd.read_csv('client_dataset.csv')

df.head()

# View the column names
column_names = df.columns

# Use the describe function to gather some basic statistics
data_description = df.describe()


# Answering questions:
# Identify the top three item categories with the most entries
top_categories = df['category_column'].value_counts().head(3)


# For the category with the most entries, identify the subcategory with the most entries
most_entries_category = top_categories.index[0]
subcategory_most_entries = df[df['category_column'] == most_entries_category]['subcategory_column'].value_counts().index[0]

# Identify the top 5 clients with the most entries in the data and store their client IDs in a list
top_clients = df['client_id_column'].value_counts().head(5).index.tolist()


# Find out how many total units the client with the most entries ordered
client_with_most_entries = top_clients[0]
total_units_ordered = df[df['client_id_column'] == client_with_most_entries]['qty_column'].sum()

# Part 2: Transform the Data
# Create a column that calculates the subtotal for each line
df['subtotal'] = df['unit_cost_column'] * df['qty_column']


# Create a column for shipping price based on your criteria
df['shipping_price'] = df['qty_column'] * 0.05


# Create a column for the total price including sales tax
df['total_price'] = df['subtotal'] + df['shipping_price'] * 1.075


# Create a column for the cost of each line
df['line_cost'] = df['unit_cost_column'] * df['qty_column']

# Create a column for the profit of each line
df['line_profit'] = df['total_price'] - df['line_cost']


# Part 3: Confirm Your Work
# Check if the calculated total prices match the given Order IDs
order_ids = df['order_id_column'].unique()
for order_id in order_ids:
    total_price = df[df['order_id_column'] == order_id]['total_price'].sum()
    print("Order ID: {} | Total Price: {}".format(order_id, total_price))


# Part 4: Summarize and Analyze
# Calculate total revenue from each of the top 5 clients
client_revenues = df[df['client_id_column'].isin(top_clients)].groupby('client_id_column')['total_price'].sum()


# Create a summary DataFrame
summary_df = pd.DataFrame({
    'Total Units Purchased': df[df['client_id_column'].isin(top_clients)].groupby('client_id_column')['qty_column'].sum(),
    'Total Shipping Price': df[df['client_id_column'].isin(top_clients)].groupby('client_id_column')['shipping_price'].sum(),
    'Total Revenue': client_revenues,
    'Total Profit': df[df['client_id_column'].isin(top_clients)].groupby('client_id_column')['line_profit'].sum()
})

# Sort the summary DataFrame by total profit
summary_df = summary_df.sort_values(by='Total Profit', ascending=False)

# Format data and columns for presentation
summary_df = summary_df / 1000000  # Convert to millions of dollars
summary_df = summary_df.rename(columns={
    'Total Units Purchased': 'Total Units Purchased (Millions)',
    'Total Shipping Price': 'Total Shipping Price (Millions)',
    'Total Revenue': 'Total Revenue (Millions)',
    'Total Profit': 'Total Profit (Millions)'
})

# Write a brief summary of your findings
summary_text = "In this analysis, we identified the top clients in terms of quantity, calculated shipping costs, and derived revenue and profit. The top client with the most entries ordered a total of {} units.".format(total_units_ordered)

# Print or save your results
print(column_names)
print(data_description)
print(top_categories)
print(most_entries_category)
print(subcategory_most_entries)
print(top_clients)
print(total_units_ordered)
print(summary_df)
print(summary_text)
