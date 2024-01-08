import pandas as pd

# Load the dataset
df = pd.read_csv('Resources/client_dataset.csv')

# Calculate total price
df['total_price'] = df['qty'] * df['unit_price']

# Remove missing values and round percentages
df = df.dropna()
df = df.round(2)

# Find the top 3 categories with the highest total sales
top_categories = df.groupby(['category'])['total_price'].sum().nlargest(3).map('${:,.2f}'.format)

print('The top categories are:')
print(top_categories)
print()

# Find the subcategory with the most entries in the top category
top_category = top_categories.index[0]
top_subcategory = df[df['category'] == top_category].groupby(['subcategory'])['subcategory'].count().nlargest(1).index[0]

print(f'The subcategory with the most entries in the top category is: {top_subcategory}')
print()

# Find the top 5 clients with the most entries
top_clients = df['client_id'].value_counts().nlargest(5).reset_index()
top_clients.columns = ['Client ID', 'Number of Entries']

# Store the client ids of the top 5 clients
top_clients_list = top_clients['Client ID'].tolist()

# Calculate subtotal for each line
df['subtotal'] = df['unit_price'] * df['qty']

# Calculate shipping price based on unit weight
df['shipping_price'] = df['unit_weight'].apply(lambda x: 7 if x > 50 else 10)

# Calculate total price with sales tax
sales_tax_rate = 0.0925
df['total_price_with_tax'] = (df['subtotal'] + df['shipping_price']) * (1 + sales_tax_rate)

# Calculate the cost of each line
df['line_cost'] = (df['unit_cost'] * df['qty']) + df['shipping_price']

# Calculate the profit of each line
df['line_profit'] = df['total_price_with_tax'] - df['line_cost']

# Confirm the calculated total prices match the given Order IDs
order_checks = {
    'Order ID 2742071': 152811.89,
    'Order ID 2173913': 162388.71,
    'Order ID 6128929': 923441.25
}

for order_id, expected_price in order_checks.items():
    order_number = int(order_id.split()[-1])
    calculated_price = df[df['order_id'] == order_number]['total_price_with_tax'].sum()
    print('Order Checks:')
    print()
    print(f"We checked the order ID {order_id} and found that the calculated price is ${calculated_price:.2f}, "
          f"while the expected price is ${expected_price:.2f}")
    print()

# Print out checked orders to understand the difference between calculated and expected prices
print("Checked Orders:")
checked_orders = df[df['order_id'].isin(order_checks.keys())].groupby('order_id')['total_price_with_tax'].sum().map('${:.2f}'.format)
print(checked_orders)
print()

# Calculate total revenue from each of the top 5 clients
client_revenues = df[df['client_id'].isin(top_clients_list)].groupby('client_id')['total_price_with_tax'].sum().map('${:,.2f}'.format)

# Calculate the total profit from each of the top 5 clients
client_profits = df[df['client_id'].isin(top_clients_list)].groupby('client_id')['line_profit'].sum().map('${:,.2f}'.format)


# Summarize the data for the top 5 clients for revenue and profit
summary_df = pd.concat([client_revenues, client_profits], axis=1)
summary_df.columns = ['Total Revenue', 'Total Profit']

# Sort the summary DataFrame by total profit
summary_df = summary_df.sort_values(by='Total Profit', ascending=False)

# Print the summary DataFrame
print(summary_df)
print()

# Filter the data to include only the top 5 clients
top_clients_data = df[df['client_id'].isin(top_clients_list)]

# Create a new DataFrame for top clients' order details
# Filter the data to include only the top 5 clients
top_clients_data = df[df['client_id'].isin(top_clients_list)]

# Create a new DataFrame for top clients' order details
top_clients_orders_df = top_clients_data.groupby(['client_id', 'order_id']).agg({
    'qty': 'sum', 
    'subtotal': 'sum', 
    'shipping_price': 'sum', 
    'total_price_with_tax': 'sum'
}).reset_index()

# Rename columns for clarity
top_clients_orders_df.columns = ['Client ID', 'Order ID', 'Total Quantity', 'Total Subtotal', 'Total Shipping Price', 'Total Price with Tax']

# Format currency columns to dollars
currency_columns = ['Total Subtotal', 'Total Shipping Price', 'Total Price with Tax']
top_clients_orders_df[currency_columns] = top_clients_orders_df[currency_columns].applymap('${:,.2f}'.format)

# Print out the top 5 clients' order details
print("Top 5 Clients Order Details:")
print(top_clients_orders_df)
print()


# Rename columns for clarity
top_clients_orders_df.columns = ['Client ID', 'Order ID', 'Total Quantity', 'Total Subtotal', 'Total Shipping Price', 'Total Price with Tax']

# Print out the top 5 clients' order details
print("Top 5 Clients Order Details:")
print(top_clients_orders_df)
print()


# Print a brief summary of findings
total_units_ordered = df[df['client_id'].isin(top_clients_list)]['qty'].sum()
summary_text = f"In this analysis, we identified the top clients in terms of quantity, calculated shipping costs, and derived revenue and profit. The top client with the most entries ordered a total of {total_units_ordered} units."
print(summary_text)
print()
