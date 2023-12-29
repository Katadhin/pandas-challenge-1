import pandas as pd

# Part 1: Explore the Data
# Import the data from the CSV file from resources folder
data = pd.read_csv('Resources/client_dataset.csv')

data.head()

# View the column names
column_names = data.columns

# Use the describe function to gather some basic statistics
data_description = data.describe()

print(data_description)
print(column_names)
print()

# Check the data types of each column to ensure they are appropriate.
# For example, numerical columns should be of type int or float, and categorical columns should be of type object.
print(data.dtypes)
print()


print(data.isnull().sum())
print()

# Check the unique values in categorical columns to understand the variety of categories or subcategories present.
print(data['category'].unique())
print()

# check data for unusual patterns or outliers.
print(data['qty'].describe())
print()


''' data check: 

1. Data Types: Check the data types of each column to ensure they are appropriate. 
For example, numerical columns should be of type int or float, and categorical columns should be of type object.

2. Missing Values: Determine if there are any missing values in the dataset and how they are distributed across columns. You can use the .isnull() and .sum() functions to count missing values.

3. Unique Values: Explore the unique values in categorical columns to understand the variety of categories or subcategories present.

4. Data Distribution: Visualize the distribution of numerical columns using histograms or box plots to identify any outliers or unusual patterns.

Correlations: Compute and visualize correlations between numerical columns to understand if there are any strong relationships between variables.
Data Range: Check the range of dates or timestamps in the dataset if applicable. This can help identify the time span covered by the data.
Data Exploration: Explore specific aspects of the data related to the questions or tasks you need to address in the project. For example, if you're analyzing sales data, you might want to look at trends over time or seasonality.
Data Quality: Assess the overall data quality. Look for anomalies or data inconsistencies that might require cleaning or preprocessing.
Summary Statistics: Calculate additional summary statistics that are relevant to your analysis, such as the mean, median, and standard deviation of specific columns.
Data Visualization: Create visualizations, such as bar charts, scatter plots, or heatmaps, to gain insights and make it easier to communicate findings. 
'''


# Answering questions:
# Identify the top three item categories with the most entries
top_categories = data['category'].value_counts().head(3)
print(top_categories) # print the top 3 categories
print()

























