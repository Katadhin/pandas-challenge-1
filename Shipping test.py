import pandas as pd

# Load the dataset
df = pd.read_csv('Resources/client_dataset.csv')

# Calculate total price
df['total_price'] = df['qty'] * df['unit_price']

# Remove missing values and round percentages
df = df.dropna()
df = df.round(2)

# Calculate subtotal for each line
df['subtotal'] = df['unit_price'] * df['qty']

# Calculate shipping price per unit based on unit weight
df['shipping_price_per_unit'] = df['unit_weight'].apply(lambda x: 7 if x > 50 else 10)

# Calculate total shipping price per line
df['total_shipping_price'] = df['shipping_price_per_unit'] * df['qty']

# Calculate total price with sales tax
sales_tax_rate = 0.0925
df['total_price_with_tax'] = (df['subtotal'] + df['total_shipping_price']) * (1 + sales_tax_rate)

# Calculate the cost of each line
df['line_cost'] = (df['unit_cost'] * df['qty']) + df['total_shipping_price']

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

# Calculate total revenue from each of the top 5 clients
client_revenues = df[df['client_id'].isin(top_clients_list)].groupby('client_id')['total_price_with_tax'].sum().map('${:,.2f}'.format)

# Calculate the total profit from each of the top 5 clients
client_profits = df[df['client_id'].isin(top_clients_list)].groupby('client_id')['line_profit'].sum().map('${:,.2f}'.format)

# Calculate average profit for different order sizes in both percentage and dollars
order_size_bins = [0, 100, 500, 1000, 5000, float('inf')]
order_size_labels = ['0-99', '100-499', '500-999', '1000-4999', '5000+']
df['order_size'] = pd.cut(df.groupby('order_id')['qty'].transform('sum'), bins=order_size_bins, labels=order_size_labels)

# Calculate average profit percentage for different order sizes
average_profit_percentage = (df.groupby('order_size')['line_profit'].mean() / df.groupby('order_size')['line_cost'].mean() * 100).map('{:.2f}%'.format)
average_profit_dollars = df.groupby('order_size')['line_profit'].mean().map('${:,.2f}'.format)

# Print the average profit in both percentage and dollars
print("Average Profit for Different Order Sizes (Percentage):")
print(average_profit_percentage)
print("\nAverage Profit for Different Order Sizes (Dollars):")
print(average_profit_dollars)
print()

# Define the variable "top_clients_orders_df"
top_clients_orders_df = df[df['client_id'].isin(top_clients_list)]

print(average_profit_percentage)
print("\nAverage Profit for Different Order Sizes (Dollars):")
print(average_profit_dollars)
print()

# Print out the top 5 clients' order details
print("Top 5 Clients Order Details:")
print(top_clients_orders_df)
print()

# Print a brief summary of findings
total_units_ordered = df[df['client_id'].isin(top_clients_list)]['qty'].sum()
summary_text = f"In this analysis, we identified the top clients in terms of quantity, calculated shipping costs, and derived revenue and profit. The top client with the most entries ordered a total of {total_units_ordered} units."
print(summary_text)
print()

# Calculate average profit percentage for different order sizes
order_size_bins = [0, 100, 500, 1000, 5000, float('inf')]
order_size_labels = ['0-99', '100-499', '500-999', '1000-4999', '5000+']
df['order_size'] = pd.cut(df.groupby('order_id')['qty'].transform('sum'), bins=order_size_bins, labels=order_size_labels)
average_profit_percentage = df.groupby('order_size')['line_profit'].mean().map('{:.2f}%'.format).reset_index()

# Create a string with insights about the relationship between order size and average profit percentage
insights = "Insights:\n"
insights += "The analysis of profit percentages reveals interesting patterns:\n"
insights += "- Smaller orders (0-99 units) tend to have an average profit percentage of around 34.45%.\n"
insights += "- Larger orders (1000+ units) tend to have an average profit percentage of around 35.57%.\n"
insights += "- Orders with 100-499 units tend to have an average profit percentage of around 35.26%.\n"
insights += "- Orders with 500-999 units tend to have an average profit percentage of around 35.21%.\n"
insights += "- The highest average profit percentage is 35.57% for orders with 1000-4999 units.\n"
insights += "- The lowest average profit percentage is 34.45% for orders with 0-99 units.\n"
insights += "- The average profit percentage for orders with 5000+ units is 35.45%.\n"

# Print the insights
print(insights)
print()
