import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import calendar

crimes_df = pd.read_csv('./data/crimes.csv', parse_dates=['Date Rptd', 'DATE OCC'])
# print(crimes_df.head())
print(crimes_df.columns)

# NOTE: From this we can see that the 'Date Rptd' and 'DATE OCC' columns are now datetime objects
print(crimes_df.dtypes)

# print(crimes_df['TIME OCC'].head(10))
# testing for correlation
# sns.heatmap(crimes_df.corr(numeric_only=True), annot=True)
# NOTE: No correlation found

# PROBLEM: Which race suffers from more violence across the state?
# sns.countplot(data=crimes_df, x='Vict Descent')
#PROBLEM: The plot contains a lot of negligible data


# PROBLEM: A lot of repetitive code is used in the exploring the dataset
def plot_top_categories(df, column, title,  xlabel, ylabel, ax, top_n = 7, palette='viridis', order=None,):
    top_categories = df[column].value_counts().nlargest(top_n).index
    filtered_df = df[df[column].isin(top_categories)]
    sns.countplot(data=filtered_df, x=column, hue=column, palette=palette ,order=top_categories, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)




# SOLUTION: Getting the t7
TOP_CATEGORIES_COUNT = 7

fig,ax = plt.subplots(figsize=(10,10))

plot_top_categories(df=crimes_df,column='Vict Descent', title="Plot showing the races most affected by crime in LA", xlabel="Race", ylabel="Number of affected individuals", ax=ax,)


# plt.show()

crimes_df['age_group'] = pd.cut(crimes_df['Vict Age'],
                          bins=[0, 18, 30, 50, 65, 100],
                          labels=['0-18', '19-30', '31-50', '51-65', '66+'])

fig2,ax2 = plt.subplots(figsize=(10,10))

sns.countplot(data=crimes_df, x='age_group', hue='age_group', palette='viridis', ax=ax2)
ax2.set_title('Age groups affected by crime')
ax2.set_xlabel('Age group')


# PROBLEM: Which area experiences the most crime?
fig3, ax3 = plt.subplots(figsize=(10,10))

plot_top_categories(df=crimes_df,column='AREA NAME', title='Plot showing the most dangerous areas in LA', xlabel='AREA NAME', ylabel='Number of occurrences', ax=ax3, palette='coolwarm')

# SOLUTION : Getting the months of the crime
crimes_df['MONTH OCC'] = crimes_df['DATE OCC'].dt.month
crimes_df['MONTH NAME'] = crimes_df['DATE OCC'].dt.month_name()

fig4, ax4 = plt.subplots(figsize=(12,6))
sns.countplot(data=crimes_df, x='MONTH NAME',ax=ax4, hue='MONTH OCC', palette="plasma", order=calendar.month_name[1:])
ax4.set_xlabel('Month')
ax4.set_title('Number of crimes committed in each month in Los Angeles')

crimes_df['HOUR OCC'] = crimes_df['TIME OCC'].transform( lambda x : x // 100)
# crimes_df['HOUR OCC'] = crimes_df['TIME OCC'] // 100 NOTE: This is an equivalent solution

# Define a time frame instead of a single hour
evening_data = crimes_df[(crimes_df['HOUR OCC'] >= 18) | (crimes_df['HOUR OCC'] < 4)]

fig5, ax5 = plt.subplots(figsize=(12, 10))
plot_top_categories(
    df=evening_data,
    column='AREA NAME',
    title='Top areas with crimes between 18:00 and 03:59',
    xlabel='Area',
    ylabel='Number of crimes',
    ax=ax5,
    palette='magma'
)
ax5.tick_params(axis='x', rotation=45)

fig6, ax6 = plt.subplots(figsize=(12, 6))
sns.histplot(data=crimes_df, x='HOUR OCC', bins=24, ax=ax6, color='steelblue', kde=False, )
ax6.set_title('Distribution of crimes by hour of day in Los Angeles')
ax6.set_xlabel('Hour of day (0-23)')
ax6.set_ylabel('Number of crimes')
ax6.set_xticks(range(0, 24))

hourly_counts = crimes_df['HOUR OCC'].value_counts().sort_index()



fig7, ax7 = plt.subplots(figsize=(12, 6))
sns.lineplot(x=hourly_counts.index, y=hourly_counts.values, ax=ax7, marker='o', color='crimson')
ax7.set_title('Crime frequency throughout the day')
ax7.set_xlabel('Hour of day')
ax7.set_ylabel('Number of crimes')
ax7.set_xticks(range(0, 24))
ax7.grid(True, alpha=0.3)

# NOTE: Slight increase in crime on Fridays but no noticeable insight seen across the days of the week

'''
crimes_df['DAY OCC'] = crimes_df['DATE OCC'].dt.day_name()
print(crimes_df['DAY OCC'].dtype, crimes_df['DAY OCC'].head())
sns.countplot(data=crimes_df, x='DAY OCC', ax=ax8, palette='viridis', hue='DAY OCC', order=calendar.day_name[0:])
ax8.set_title('Crimes across the week')
ax8.set_xlabel('Day of the week')
ax8.set_ylabel('Count')
'''


fig8,ax8 = plt.subplots(figsize=(15,20))
plot_top_categories(df=crimes_df, column='Crm Cd Desc', title='Types of crime committed', xlabel='Crime type', ylabel='Number of occurrences', ax=ax8, palette='viridis')
ax8.tick_params(axis='x', rotation=60, labelsize=8)


# PROBLEM: How many percentage of crimes have been resolved
print(crimes_df['Status Desc'].value_counts(normalize=True))
# IMPORTANT: 82% of crimes are still unresolved!

# PROBLEM: What percent of crimes involve a weapon
crimes_df['Weapon Used'] = crimes_df['Weapon Desc'].notna().map({True: 'Weapon', False: 'No weapon'})
print(crimes_df['Weapon Used'].value_counts(normalize=True))
# IMPORTANT: 60% of crimes involved a weapon.

# PROBLEM: What types of crimes are males and females most subject to?
top_crimes = crimes_df['Crm Cd Desc'].value_counts().nlargest(10).index
filtered = crimes_df[crimes_df['Crm Cd Desc'].isin(top_crimes) & crimes_df['Vict Sex'].isin(['M', 'F'])]

corr_table = pd.crosstab(filtered['Crm Cd Desc'], filtered['Vict Sex'], normalize='index')

fig9, ax9 = plt.subplots(figsize=(12, 12))
sns.heatmap(corr_table, annot=True, fmt='.2f', cmap='coolwarm', ax=ax9)
ax9.set_title('Top 10 crimes by victim sex')
ax9.tick_params(axis='x', rotation=45, labelsize=9)

# IMPORTANT: at least 40% of crimes in each area are committed at night
night_share = evening_data['AREA NAME'].value_counts() / crimes_df['AREA NAME'].value_counts()
# print(night_share)
plt.tight_layout()
plt.show()
print(crimes_df.dtypes)
