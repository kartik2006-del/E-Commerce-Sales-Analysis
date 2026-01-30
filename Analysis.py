import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_csv(r'C:\Users\KARTIK\.ipython\clean_dataset.csv',encoding='latin1')

# DATA CLEANING

# First handle the null by  using
df.isna().sum() # it shows total null values from each column

# go for duplicate
df.duplicated().sum() #it shows total duplicate values from whole data set
df[df.duplicated()] #show duplicate from each column
df=df.drop_duplicates() #removing duplicate

# handling profits
def profit_tracker(x):
    if x['Profit']>0:
        return 'Healthy Orders'
    else:
        return 'Loss Making' 
df['Profit_tracker']=df.apply(profit_tracker,axis=1)

# SALES ANALYSIS :

# Q-define Total Sales
print(np.round(df['Sales'].sum(),decimals=2)) # the company generated total sales of ₹2296919.49 during the observed period, indicating the overall scale of business operations

# Q-Monthly Sales Trend
df['Order Date']=pd.to_datetime(df['Order Date'],errors='coerce')
df['Month_num']=df['Order Date'].dt.month
df['Month']=df['Order Date'].dt.month_name()
Monthly_sales=df.groupby(['Month_num','Month'])['Sales'].sum().reset_index().sort_values('Month_num')# aggregate before plotting to control order & readability
print(Monthly_sales)
    #graph analysis
sns.barplot(data=Monthly_sales,x='Month',y='Sales')
plt.xlabel('Month')
plt.ylabel('Total_Sales')
plt.title('Monthly Sales Trend ')
plt.xticks(rotation=46)
plt.savefig("monthly_sales.png", bbox_inches='tight')
plt.show() # overall November month is good for sales compare other months

# Q- Sales by category
Category_sales=np.round(df.groupby('Category')['Sales'].
                        sum().
                        reset_index(),
                        decimals=2)

print(Category_sales)
    # graph analysis
sns.barplot(data=Category_sales,x='Category',y='Sales')
plt.xlabel('Category')
plt.ylabel('Total_Sales')
plt.title('Category Sales Trend ')
plt.xticks(rotation=46) # the category-technology has maximum sales 
plt.savefig('category_sales.png',dpi=300)
plt.show()

# profit analysis
# Q-profit by category and sub category
Category_profit=np.round(df.groupby('Category')['Profit']
                         .sum()
                         .reset_index(),decimals=2
                         )
print(Category_profit)

sns.barplot(data=Category_profit,x='Category',y='Profit')
plt.xlabel('Category')
plt.ylabel('Profit')
plt.title('Profit by Category')
plt.savefig('profit by category.png',bbox_inches='tight')
plt.show()
Sub_Category_profit=np.round(df.groupby('Sub-Category')['Profit'].
                             sum().
                             reset_index(),
                             decimals=2)
print(Sub_Category_profit)

sns.barplot(data=Sub_Category_profit,x='Sub-Category',y='Profit')
plt.xlabel('Sub-Category')
plt.ylabel('Profit')
plt.title('Profit by Sub-Category')
plt.xticks(rotation=45)
plt.savefig('profit by sub-category.png',bbox_inches='tight')
plt.show()

# Q-define loss making product
loss_df = df[df['Profit_tracker'] == 'Loss Making'] # first,i isolate only loss-making orders to focus on promblem areas
print(loss_df.shape)

category_loss = (
    loss_df.groupby('Category')['Profit']
    .sum()
    .reset_index()
    .sort_values(by='Profit')
)

print(category_loss)
sns.barplot(data=category_loss, x='Category', y='Profit', palette='Reds')
plt.title('Loss by Category')
plt.ylabel('Total Loss')
plt.xlabel('Category')
plt.savefig('loss by category.png',bbox_inches='tight')
plt.show()
# * furniture category is ccontributing the highest overall loss
#  * technology and office supllies are relatively stable 

sub_category_loss = (
    loss_df.groupby('Sub-Category')['Profit']
    .sum()
    .reset_index()
    .sort_values(by='Profit')
)
print(sub_category_loss.head())
plt.figure(figsize=(10,5))
sns.barplot(
    data=sub_category_loss.head(10),
    x='Sub-Category',
    y='Profit',
    palette='Reds'
)
plt.xticks(rotation=45)
plt.title('Top Loss-Making Sub-Categories')
plt.savefig('top loss making sub-category.png',dpi=300)
plt.show()
# although furniture overall is loss making ,sub-categories like tables and bookcases are in the major contributors

total_loss = sub_category_loss['Profit'].sum()

sub_category_loss['Loss_Percentage'] = (
    sub_category_loss['Profit'] / total_loss * 100
)

print(sub_category_loss.head()) # top-3 sub-categories alone contribute more than 60% of total losses

profit_summary = (
    df.groupby('Profit_tracker')['Profit']
    .sum()
    .reset_index()
)

sns.barplot(data=profit_summary, x='Profit_tracker', y='Profit')
plt.title('Profit vs Loss Orders')
plt.savefig('profit vs loss orders.png',dpi=300)
plt.show()

# high quantity VS low profit analysis
Summary =df.groupby('Sub-Category')[['Quantity','Profit']].sum().reset_index()
print(Summary)
avg_quantity=Summary['Quantity'].mean()
problem_products=Summary[(Summary['Quantity']>avg_quantity) & (Summary['Profit']<0)
]
sns.scatterplot(data=Summary,x='Quantity',y='Profit')
plt.axhline(0)
plt.xlabel('Quantity')
plt.ylabel('Profit')
plt.title('high quantity V/S low profit')
plt.savefig('high quantity VS low profit.png',dpi=300)
plt.show()
# I identified sub-categories with above-average sales volume but negative profitability, indicating margin erosion despite high demand

# DATA VISUALIZATION

# - Profit Outliers
plt.figure(figsize=(6,4))
sns.boxplot(y=df['Profit'])
plt.title('Profit Distribution with Outliers')
plt.ylabel('Profit')
plt.savefig('profit distribution with ordres.png',dpi=300)
plt.show()

# category vs sub-category heatmap
heatmap_data=df.groupby(['Category','Sub-Category'])['Profit'].sum().reset_index().pivot(index=
'Category',columns='Sub-Category',values='Profit')
plt.figure(figsize=(12,6))

sns.heatmap(
    heatmap_data,
    cmap='RdYlGn',        
    center=0,             
    annot=True,
    fmt='.0f',
    linewidths=0.5
)

plt.title('Profit Heatmap: Category vs Sub-Category')
plt.xlabel('Sub-Category')
plt.ylabel('Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Heatmap.png',dpi=300)
plt.show()

# INSIGHTS & FINDING
# Q-which category is most profitable
# ANS- Technology is the most profitable category,contributing the highest overall profit.The technology indicates the strong margins compare to other category
# Q-Seasonal sales pattern
# ANS-Sales paek during November-December,while early-year months show weaker performance,indicating strong seasonality driven by festive demand
# Q-Business recommendations based on data
# ANS- 1 Optimize or phase out loss-making sub-categories
#       Sub-categories like Bookcases generate consistent losses despite sales volume.
#       Action: Reduce discounts, renegotiate supplier costs, or discontinue low-margin SKUs.
#    2 Focus on peak seasonal demand 
        # November shows the highest sales, indicating strong seasonality.
        # Action : Increase inventory, targeted promotions, and marketing spend during peak months to maximize revenue.
#    3 Shift strategy from high volume to high profit
        #Some products have high quantity sold but negative profit, indicating margin erosion.
        # Action: Reprice products and control logistics costs instead of pushing volume.
# 4 Strengthen profitable categories
    #Technology category consistently delivers higher profit.
    #Action: Allocate more resources and cross-sell profitable tech products to improve overall margins.
