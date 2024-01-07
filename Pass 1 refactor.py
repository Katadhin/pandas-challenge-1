#Pass 1 Refactor from ChatGpt 4 
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
