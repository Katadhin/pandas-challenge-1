# Part 2 Pass 1 - Explore the Data
import pandas as pd

# Part 1: Explore the Data
# Import the data from the CSV file (assuming the file is in the same directory as this script)
data = pd.read_csv('client_dataset.csv')

# Display the first few rows of the dataset to get an overview
print("First few rows of the dataset:")
print(data.head())
print()

# View the column names
column_names = data.columns
print("Column names:")
print(column_names)
print()

# Use the describe function to gather basic statistics of numerical columns
data_description = data.describe()
print("Basic statistics of numerical columns:")
print(data_description)
print()

# Check the data types of each column
print("Data types of columns:")
print(data.dtypes)
print()

# Check for missing values in each column
missing_values = data.isnull().sum()
print("Missing values in each column:")
print(missing_values)
print()

# Explore unique values in the 'category' column
unique_categories = data['category'].unique()
print("Unique values in the 'category' column:")
print(unique_categories)
print()

# Explore the distribution of the 'qty' column
qty_distribution = data['qty'].describe()
print("Distribution of the 'qty' column:")
print(qty_distribution)
print()

# Answering questions:
# Identify the top three item categories with the most entries
top_categories = data['category'].value_counts().head(3)
print("Top three item categories with the most entries:")
print(top_categories)

# Part 2: Transform the Data
# Create a column that calculates the subtotal for each line
data['subtotal'] = data['unit_cost'] * data['qty']
print("Subtotal column:")
print(data['subtotal'])
print()


# Create a column for shipping price based on your criteria
data['shipping_price'] = data['qty'] * 0.05
print("Shipping price column:")
print(data['shipping_price'])
print()

# Create a column for the total price including sales tax rounded to two decimal places
data['total_price'] = data['subtotal'] + data['shipping_price'] * 1.075
data['total_price'] = data['total_price'].round(2)
print("Total price column:")
print(data['total_price'])
print()

# Create a column for the cost of each line
data['line_cost'] = data['unit_cost'] * data['qty']
print("Line cost column:")
print(data['line_cost'])
print()

# Create a column for the profit of each line
data['line_profit'] = data['total_price'] - data['line_cost']
print("Line profit column:")
print(data['line_profit'])
print()

# Display the first few rows of the dataset to confirm the changes
print("First few rows of the dataset:")
print(data.head())
print()

# Find the most profitable customers
order_ids = [1, 2, 3, 4, 5]  # Replace [1, 2, 3, 4, 5] with the actual list of order IDs
print("Most profitable customers:")
print(data.groupby('client_id')['line_profit'].sum().sort_values(ascending=False).head(5))
print()

# Compare the calculated total prices with the given Order IDs
# Find exceptions where the calculated total price does not match the given total price
print("Exceptions where the calculated total price does not match the given total price:")
print(data[data['order_id'].isin(order_ids)].groupby('order_id')['total_price'].sum())
print()

# Part 4: Summarize and Analyze
# Calculate total revenue from each of the top 5 clients and round to two decimal places
#Calculate total costs from each of the top 5 clients
# Calculate total proift from each of the top 5 clients
# Calculate total units purchased from each of the top 5 clients
# Calculate total shipping price from each of the top 5 clients
# Create a summary DataFrame
# Sort the summary DataFrame by total profit
# Display the summary DataFrame
total_revenue = data.groupby('client_id')['total_price'].sum().sort_values(ascending=False).head(5)
total_cost = data.groupby('client_id')['line_cost'].sum().sort_values(ascending=False).head(5)
total_profit = data.groupby('client_id')['line_profit'].sum().sort_values(ascending=False).head(5)
total_units = data.groupby('client_id')['qty'].sum().sort_values(ascending=False).head(5)
total_shipping = data.groupby('client_id')['shipping_price'].sum().sort_values(ascending=False).head(5)
summary_df = pd.DataFrame({
    'Total Revenue': total_revenue,
    'Total Cost': total_cost,
    'Total Profit': total_profit,
    'Total Units Purchased': total_units,
    'Total Shipping Price': total_shipping
})
summary_df = summary_df.sort_values(by='Total Profit', ascending=False)
print("Summary DataFrame:")
print(summary_df)
print()















