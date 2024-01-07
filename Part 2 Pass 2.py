# Import the data and Pandas
import pandas as pd
import pandas as pd
df = pd.read_csv('Resources/client_dataset.csv')
df.head()
print(df.head())

# View the column names in the data
df.columns
print(df.columns)

# Add a total price column to the data
df['total_price'] = df['qty'] * df['unit_price']
df.head()
print(df.head())

# Use the describe function to gather some basic statistics
# about the data
df.describe()
df.columns
df.dtypes
print(df.describe())
print(df.columns)
print(df.dtypes)

# Remove rows with missing values and round percentages to 2 decimal places
df = df.dropna()
df = df.round(2)
df.head()
print(df.head())
print()

# Find the top 3 categories with the highest total sales
top_categories = df.groupby(['category'])['total_price'].sum().nlargest(3)
top_categories

# Convert the output to dollars 
top_categories = top_categories.map('${:,.2f}'.format)
top_categories
print(top_categories)
print()

# For the category with the most entries, which subcategory had the most entries?
top_category = df.groupby(['category'])['category'].count().nlargest(1)
top_category
top_subcategory = df.groupby(['subcategory'])['subcategory'].count().nlargest(1)
top_subcategory
print(top_category)
print(top_subcategory)
print()

# Which five clients had the most entries in the data?
# Output a df with the client id and the number of entries
top_clients = df.groupby(['client_id'])['client_id'].count().nlargest(5)
top_clients
top_clients = pd.DataFrame(top_clients)
top_clients
top_clients.columns = ['Number of Entries']
top_clients
top_clients.index.name = 'Client ID'
top_clients
print(top_clients)
print()

# Store the client ids of those top 5 clients in a list.
# Use that list to filter the original data
top_clients_list = top_clients.index.tolist()
top_clients_list
top_clients_df = df[df['client_id'].isin(top_clients_list)]
top_clients_df.head()
print()
print(top_clients_list)
print()
print(top_clients_df.head())
print()

# show all data for the first of those five clients
df.loc[df['client_id'] == 'CLIENT_ID_HERE']
df
print(df.loc[df['client_id'] == 'CLIENT_ID_HERE'])
print()

# Create a column that calculates the 
# subtotal for each line using the unit_price and the qty columns 
df['subtotal'] = df['unit_price'] * df['qty']
df.head()
print(df.head())
print()

# Create a column for shipping price.
# Assume a shipping price of $7 per pound
# for orders over 50 pounds and $10 per
# pound for items 50 pounds or under.
# Use the weight column to calculate this.
df['shipping_price'] = df['unit_weight'].apply(lambda x: 7 if x > 50 else 10)
df.head()
print(df.head())
print()

# Create a column for the total price
# using the subtotal and the shipping price
# along with a sales tax of 9.25%
df['total_price'] = df['subtotal'] + df['shipping_price'] * 1.0925
df.head()
print(df.head())
print()

# Create a column for the cost
# of each line using unit cost, qty, and
# shipping price (assume the shipping cost
# is exactly what is charged to the client)
df['line_cost'] = df['unit_cost'] * df['qty'] + df['shipping_price']
df.head()
print(df.head())
print()

# Create a column for the profit of
# each line using line cost and line price
df['line_profit'] = df['total_price'] - df['line_cost']
df.head()
print(df.head())
print()

# Update the top_clients_df to include shipping price and profit
top_clients_df['shipping_price'] = top_clients_df['unit_weight'].apply(lambda x: 7 if x > 50 else 10)
top_clients_df['line_cost'] = top_clients_df['unit_cost'] * top_clients_df['qty'] + top_clients_df['shipping_price']
top_clients_df['line_profit'] = top_clients_df['total_price'] - top_clients_df['line_cost']
top_clients_df.head()
print(top_clients_df.head())
print()

## Part 3: Confirm your work
# You have email receipts showing that the total prices for 3 orders. Confirm that your calculations match the receipts. Remember, each order has multiple lines.
# Order ID 2742071 had a total price of \$152,811.89
# Order ID 2173913 had a total price of \$162,388.71
# Order ID 6128929 had a total price of \$923,441
# Check if the calculated total prices match the given Order IDs
order_checks = {
    'Order ID 2742071': 152811.89,
    'Order ID 2173913': 162388.71,
    'Order ID 6128929': 923441.25
}

for order_id, expected_price in order_checks.items():
    calculated_price = df[df['order_id'] == int(order_id.split()[-1])]['total_price'].sum()
    print(f'{order_id} - Calculated Price: ${calculated_price:.2f}, Expected Price: ${expected_price:.2f}')
print()


# How much did each of the top 5 clients by quantity
# spend? Check your work from Part 1 for client ids.
# Calculate total revenue from each of the top 5 clients
client_revenues = df[df['client_id'].isin(top_clients_list)].groupby('client_id')['total_price'].sum()


# Display as dollars with 2 decimal places
client_revenues = client_revenues.map('${:,.2f}'.format)
client_revenues
print(client_revenues)
print()

# Summarize the data for the top 5 clients and display as dollars
top_clients_df.groupby(['client_id']).agg({'total_price': ['sum', 'mean', 'min', 'max']}).round(2).map('${:,.2f}'.format)

# Create a summary DataFrame with the total units purchased, total shipping price, total revenue, and total profit for each of the top 5 clients
summary_df = pd.DataFrame({
    'Total Units Purchased (Millions)': df[df['client_id'].isin(top_clients_list)].groupby('client_id')['qty'].sum() / 1_000_000,
    'Total Shipping Price (Millions)': df[df['client_id'].isin(top_clients_list)].groupby('client_id')['shipping_price'].sum() / 1_000_000,
    'Total Revenue (Millions)': client_revenues.str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float) / 1_000_000,
    'Total Profit (Millions)': df[df['client_id'].isin(top_clients_list)].groupby('client_id')['line_profit'].sum().astype(float) / 1_000_000
})

# Format data and columns for presentation
summary_df = summary_df.round(2).applymap('${:,.2f}'.format)

# Print the summary DataFrame
print(summary_df)

# Summarize the data for the top 5 clients and display as dollars
top_clients_df.groupby(['client_id']).agg({'total_price': ['sum', 'mean', 'min', 'max']}).round(2).map('${:,.2f}'.format)

# Create a summary DataFrame with the total units purchased, total shipping price, total revenue, and total profit for each of the top 5 clients
summary_df = pd.DataFrame({
    'Total Units Purchased (Millions)': df[df['client_id'].isin(top_clients_list)].groupby('client_id')['qty'].sum() / 1_000_000,
    'Total Shipping Price (Millions)': df[df['client_id'].isin(top_clients_list)].groupby('client_id')['shipping_price'].sum() / 1_000_000,
    'Total Revenue (Millions)': client_revenues.str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float) / 1_000_000,
    'Total Profit (Millions)': df[df['client_id'].isin(top_clients_list)].groupby('client_id')['line_profit'].sum().astype(float) / 1_000_000
})

# Format data and columns for presentation
summary_df = summary_df.round(2).applymap('${:,.2f}'.format)



# sort the updated data by "Total Profit" form highest to lowest
total_units_ordered = df[df['client_id'].isin(top_clients_list)]['qty'].sum()  # Calculate the total units ordered by the top client

summary_df = summary_df.sort_values(by='Total Profit (Millions)', ascending=False)

# Print the final summary DataFrame and total units ordered by the top client
print(summary_df)
print()
print(f'Total units ordered by the top client: {total_units_ordered}')
print()



# Brief summary of findings
summary_text = f"In this analysis, we identified the top clients in terms of quantity, calculated shipping costs, and derived revenue and profit. The top client with the most entries ordered a total of {total_units_ordered} units."
print(summary_text)






























