import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and clean data
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Remove top 2.5% and bottom 2.5% of page views
lower = df['value'].quantile(0.025)
upper = df['value'].quantile(0.975)
df_cleaned = df[(df['value'] >= lower) & (df['value'] <= upper)]

def draw_line_plot():
    data = df_cleaned.copy()
    
    plt.figure(figsize=(15,5))
    plt.plot(data.index, data['value'], color='red')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    
    plt.savefig('line_plot.png')
    plt.close()

def draw_bar_plot():
    data = df_cleaned.copy()
    data['year'] = data.index.year
    data['month'] = data.index.month
    monthly_avg = data.groupby(['year', 'month'])['value'].mean().unstack()
    
    monthly_avg.plot(kind='bar', figsize=(15,7))
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(
        title='Months',
        labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    )
    plt.savefig('bar_plot.png')
    plt.close()

def draw_box_plot():
    data = df_cleaned.copy().reset_index()
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.strftime('%b')
    data['month_num'] = data['date'].dt.month
    
    # Sort months correctly
    data = data.sort_values('month_num')
    
    fig, axes = plt.subplots(1, 2, figsize=(18,6))
    
    # Year-wise Box Plot
    sns.boxplot(x='year', y='value', data=data, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    # Month-wise Box Plot
    sns.boxplot(x='month', y='value', data=data, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    
    plt.savefig('box_plot.png')
    plt.close()
