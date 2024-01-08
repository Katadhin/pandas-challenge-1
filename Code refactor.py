import pandas as pd #import pandas library

print() #print a blank line

def load_and_preview_data(file_path): #define a function to load and preview the data
    data = pd.read_csv(file_path) #load the data
    print("First 5 rows of the dataset:") #print a message
    print(data.head(), '\n') #print the first 5 rows of the data
    return data #return the data

def summarize_data(data):
    print("Column Names:")
    print(data.columns, '\n')

    print("Data Description:")
    print(data.describe().round(2), '\n')

    print("Data Types:")
    print(data.dtypes, '\n')

    print("Missing Values:")
    print(data.isnull().sum(), '\n')

    print("Unique Categories:")
    print(data['category'].unique(), '\n')

    print("Quantity Description:")
    print(data['qty'].describe().round(2), '\n')

    print("Outliers in Quantity (qty > 20000):")
    print(data[data['qty'] > 20000], '\n')


def identify_top_categories(data, num_top=3):
    top_categories = data['category'].value_counts().head(num_top)
    print(f"Top {num_top} Categories:")
    print(top_categories, '\n')

# Part 1: Explore the Data
data = load_and_preview_data('Resources/client_dataset.csv')
summarize_data(data)
identify_top_categories(data)

# Continue with further analysis...

# Function to calculate shipping price per unit
def calculate_shipping(unit_weight):
    return 7 if unit_weight > 50 else 10

print()

# Function to summarize order checks
def summarize_orders(df, order_ids):
    print("Order Checks:")
    for order_id, expected_price in order_ids.items():
        calculated_price = df[df['order_id'] == int(order_id)]['total_price_with_tax'].sum()
        print(f"Order ID {order_id}: Calculated - ${calculated_price:.2f}, Expected - ${expected_price:.2f}")
    print()

# Load and preprocess the dataset
df = pd.read_csv('Resources/client_dataset.csv').dropna().round(2)

# Calculating various prices and costs
df['total_price'] = df['qty'] * df['unit_price']
df['shipping_price_per_unit'] = df['unit_weight'].apply(calculate_shipping)
df['total_shipping_price'] = df['shipping_price_per_unit'] * df['qty']
df['subtotal'] = df['unit_price'] * df['qty']
df['total_price_with_tax'] = df.eval('(subtotal + total_shipping_price) * (1 + 0.0925)')
df['line_cost'] = df['unit_cost'] * df['qty'] + df['total_shipping_price']
df['line_profit'] = df['total_price_with_tax'] - df['line_cost']

# Order checks
order_checks = {
    '2742071': 152811.89,
    '2173913': 162388.71,
    '6128929': 923441.25
}
summarize_orders(df, order_checks)

# Analysis for average profit for different order sizes
order_size_bins = [0, 100, 500, 1000, 5000, float('inf')]
order_size_labels = ['0-99', '100-499', '500-999', '1000-4999', '5000+']
df['order_size'] = pd.cut(df.groupby('order_id')['qty'].transform('sum'), bins=order_size_bins, labels=order_size_labels)

average_profit_percentage = (df.groupby('order_size', observed=True)['line_profit'].mean() / df.groupby('order_size', observed=True)['line_cost'].mean() * 100).map('{:.2f}%'.format)
average_profit_dollars = df.groupby('order_size', observed=True)['line_profit'].mean().map('${:,.2f}'.format)


print("Average Profit for Different Order Sizes (Percentage):")
print(average_profit_percentage)
print("\nAverage Profit for Different Order Sizes (Dollars):")
print(average_profit_dollars)
print()

# Analysis for top clients (as defined earlier in the code)

# ...

# Insights about the relationship between order size and average profit percentage
insights = "Insights:\n"
insights += "The analysis of profit percentages reveals interesting patterns:\n"
insights += "- Smaller orders (0-99 units) tend to have an average profit percentage of around 34.45%.\n"
insights += "- Larger orders (1000+ units) tend to have an average profit percentage of around 35.57%.\n"
insights += "- Orders with 100-499 units tend to have an average profit percentage of around 35.26%.\n"
insights += "- Orders with 500-999 units tend to have an average profit percentage of around 35.21%.\n"
insights += "- The highest average profit percentage is 35.57% for orders with 1000-4999 units.\n"
insights += "- The lowest average profit percentage is 34.45% for orders with 0-99 units.\n"
insights += "- The average profit percentage for orders with 5000+ units is 35.45%.\n"

print(insights)
print()

# Additional analyses...





