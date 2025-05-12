import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

# Load dataset
file_path = 'WA_Fn-UseC_-HR-Employee-Attrition.csv'
df = pd.read_csv(file_path)

# Preview data
print('Dataset preview:')
display(df.head())

# Create SQLite in-memory database and load data
conn = sqlite3.connect(':memory:')
df.to_sql('employee_attrition', conn, index=False, if_exists='replace')

# Query 1: Attrition count
attrition_count = pd.read_sql_query("""
    SELECT Attrition, COUNT(*) as Count 
    FROM employee_attrition 
    GROUP BY Attrition
""", conn)

# Query 2: Attrition rate by Department
attrition_dept = pd.read_sql_query("""
    SELECT Department, 
           ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS AttritionRate
    FROM employee_attrition
    GROUP BY Department
    ORDER BY AttritionRate DESC
""", conn)

# Query 3: Average Monthly Income by Attrition
income_attrition = pd.read_sql_query("""
    SELECT Attrition, ROUND(AVG(MonthlyIncome), 2) AS AvgMonthlyIncome
    FROM employee_attrition
    GROUP BY Attrition
""", conn)

# Plotting
plt.figure(figsize=(15, 12))

# Plot 1: Attrition Count
plt.subplot(3, 1, 1)
sns.barplot(x='Attrition', y='Count', data=attrition_count, palette='Set2')
plt.title('Employee Attrition Count')
plt.ylabel('Number of Employees')

# Plot 2: Attrition Rate by Department
plt.subplot(3, 1, 2)
sns.barplot(x='Department', y='AttritionRate', data=attrition_dept, palette='Set1')
plt.title('Attrition Rate by Department (%)')
plt.ylabel('Attrition Rate (%)')
plt.xticks(rotation=45)

# Plot 3: Average Monthly Income by Attrition
plt.subplot(3, 1, 3)
sns.barplot(x='Attrition', y='AvgMonthlyIncome', data=income_attrition, palette='Set3')
plt.title('Average Monthly Income by Attrition')
plt.ylabel('Average Monthly Income')

plt.tight_layout()
plt.show()
