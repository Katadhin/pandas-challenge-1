import pandas as pd

# Load the dataset
df = pd.read_csv('Resources/client_dataset.csv')

# Calculate total price
df['total_price'] = df['qty'] * df['unit_price']

# Remove missing values and round percentages
df = df.dropna()
df = df.round(2)

# Find the top 3 categories with the highest total sales
top_categories = df.groupby(['category'])['total_price'].sum().nlargest(3)
top_categories = top_categories.map('${:,.2f}'.format)
print()
print(f'The top categories are: ')
print()
print(top_categories)
print()


# Find the subcategory with the most entries in the top category
top_category = df.groupby(['category'])['category'].count().nlargest(1).index[0]
top_subcategory = df[df['category'] == top_category].groupby(['subcategory'])['subcategory'].count().nlargest(1).index[0]
print()
print(f'The subcategory with the most entries in the top category is: {top_subcategory}')
print()

# Find the top 5 clients with the most entries
top_clients = df.groupby(['client_id'])['client_id'].count().nlargest(5)
top_clients = pd.DataFrame(top_clients)
top_clients.columns = ['Number of Entries']
top_clients.index.name = 'Client ID'

# Store the client ids of the top 5 clients
top_clients_list = top_clients.index.tolist()

# Filter the data to show all entries for the first of the top 5 clients
top_client_entries = df[df['client_id'] == top_clients_list[0]]

# Calculate subtotal for each line
df['subtotal'] = df['unit_price'] * df['qty']

# Calculate shipping price based on unit weight
df['shipping_price'] = df['unit_weight'].apply(lambda x: 7 if x > 50 else 10)

# Calculate total price with sales tax
df['total_price'] = df['subtotal'] + df['shipping_price'] * 1.0925

# Calculate the cost of each line
df['line_cost'] = df['unit_cost'] * df['qty'] + df['shipping_price']

# Calculate the profit of each line
df['line_profit'] = df['total_price'] - df['line_cost']

# Create a copy of top_clients_df
top_clients_df = df[df['client_id'].isin(top_clients_list)].copy()

# Update the top_clients_df to include shipping price and profit
top_clients_df['shipping_price'] = top_clients_df['unit_weight'].apply(lambda x: 7 if x > 50 else 10)
top_clients_df['line_cost'] = top_clients_df['unit_cost'] * top_clients_df['qty'] + top_clients_df['shipping_price']
top_clients_df['line_profit'] = top_clients_df['total_price'] - top_clients_df['line_cost']

# Confirm the calculated total prices match the given Order IDs
order_checks = {
    'Order ID 2742071': 152811.89,
    'Order ID 2173913': 162388.71,
    'Order ID 6128929': 923441.25
}

for order_id, expected_price in order_checks.items():
    calculated_price = df[df['order_id'] == int(order_id.split()[-1])]['total_price'].sum()
    print(f'We checked the order ID {order_id} and found that the calculated price is ${calculated_price:.2f}, while the expected price is ${expected_price:.2f}')
    print(f'{order_id} - Calculated Price: ${calculated_price:.2f}, Expected Price: ${expected_price:.2f}')
    print
print() 


# Calculate total revenue from each of the top 5 clients
client_revenues = df[df['client_id'].isin(top_clients_list)].groupby('client_id')['total_price'].sum()
client_revenues = client_revenues.map('${:,.2f}'.format)
print()

# Summarize the data for the top 5 clients
summary_df = pd.DataFrame({
    'Total Units Purchased': df[df['client_id'].isin(top_clients_list)].groupby('client_id')['qty'].sum(),
    'Total Shipping Price': df[df['client_id'].isin(top_clients_list)].groupby('client_id')['shipping_price'].sum(),
    'Total Revenue': client_revenues.str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float),
    'Total Profit': df[df['client_id'].isin(top_clients_list)].groupby('client_id')['line_profit'].sum().astype(float)
})

# Format data and columns for presentation
summary_df['Total Units Purchased'] = summary_df['Total Units Purchased'].apply('{:,.0f}'.format)
summary_df[['Total Shipping Price', 'Total Revenue', 'Total Profit']] = summary_df[
    ['Total Shipping Price', 'Total Revenue', 'Total Profit']].applymap('${:,.2f}'.format)

# Sort the summary DataFrame by total profit
summary_df = summary_df.sort_values(by='Total Profit', ascending=False)

# Print the summary DataFrame with skipped lines
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(summary_df)
    print()

# Print a brief summary of findings
total_units_ordered = df[df['client_id'].isin(top_clients_list)]['qty'].sum()
summary_text = f"In this analysis, we identified the top clients in terms of quantity, calculated shipping costs, and derived revenue and profit. The top client with the most entries ordered a total of {total_units_ordered} units."
print(summary_text)
print()

