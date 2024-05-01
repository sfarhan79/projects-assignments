import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

finance_sectors=pd.read_excel("Financial Performance of Sectors.xlsx")
finance_sectors

# **Exploratory Data Analysis (EDA)**

# replace Null values in Discount Band with "No Discount"
finance_sectors['Discount Band'].fillna('No Discount', inplace=True)

finance_sectors.info()

finance_sectors.shape

finance_sectors.size

finance_sectors.describe()

finance_sectors.columns

finance_sectors['Segment'].value_counts()

finance_sectors['Country'].value_counts()

print("Most active Country in business:",finance_sectors["Country"].value_counts().idxmax())

print("Segment with least sales:",finance_sectors['Segment'].value_counts().idxmin())

# Product with the highest manufacturing price.
highest_price_product, highest_price = finance_sectors[finance_sectors['Manufacturing Price'] == finance_sectors['Manufacturing Price'].max()][['Product', 'Manufacturing Price']].values[0]
print(f"Product with the highest manufacturing price: {highest_price_product}, Price: {highest_price}")

# Segment with the lowest COGS.
lowest_cogs_segment = finance_sectors.loc[finance_sectors['COGS'].idxmin(), 'Segment']
lowest_cogs_value = finance_sectors.loc[finance_sectors['COGS'].idxmin(), 'COGS']

print(f"Segment with the lowest COGS: {lowest_cogs_segment}, COGS value: {lowest_cogs_value}")

# Country with the best Sale Price.
best_sale_price_country = finance_sectors.groupby('Country')['Sale Price'].mean().sort_values(ascending=False).index[0]
best_sale_price_value = finance_sectors.groupby('Country')['Sale Price'].mean().sort_values(ascending=False).values[0]

print(f"Country with the best selling price: {best_sale_price_country}, Average selling price: {np.round(best_sale_price_value,2)}")

# **Data Visualization**

# Products' Unit Sales
sns.barplot(x = 'Units Sold', y = 'Product' , data = finance_sectors, palette="inferno", hue='Product', legend=False)
plt.xticks(rotation=90)
plt.show()

# Pie chart for the Segment with highest Sales.
sales_by_segment = finance_sectors.groupby('Segment')['Units Sold'].sum()
highest_sales_segment = sales_by_segment.idxmax()
highest_sales_value = sales_by_segment.max()

labels = sales_by_segment.index.to_list()
colors = sns.color_palette('husl', len(labels))

explode = [0] * len(labels)
explode[labels.index(highest_sales_segment)] = 0.1

plt.pie(sales_by_segment, labels=labels, colors=colors, autopct='%.1f%%', explode=explode, shadow=True, startangle=90)
plt.title(f'Segment with the Highest Sales: {highest_sales_segment}')
plt.show()

# Line graph to analyze the Country with high profits
finance_sectors['Profit'] = finance_sectors['Units Sold'] * (finance_sectors['Sale Price'] - finance_sectors['Manufacturing Price'])
profit_by_country = finance_sectors.groupby('Country')['Profit'].sum()

highest_profit_country = profit_by_country.idxmax()

plt.figure(figsize=(15,4))
profit_by_country.plot(kind='line', color='green')
plt.title('Profit by Country')
plt.xlabel('Country')
plt.ylabel('Profit')

# Add annotation for the country with the highest profit
plt.annotate(f'{highest_profit_country}: {profit_by_country[highest_profit_country]}', xy=(1, profit_by_country[highest_profit_country]), xytext=(25, 0),
             xycoords=('axes fraction', 'data'), textcoords='offset points',
             arrowprops=dict(arrowstyle='-|>'))

plt.show()

# A displot showing the most Profitable Month/s for Segments
plt.figure(figsize=(30,10))
sns.displot(x="Month Name", hue="Segment", data=finance_sectors, palette="viridis", kde=True)
plt.title("Most Profitable Month for Each Segment", fontsize=16, color='darkblue')
plt.xlabel("Month", fontsize=14, color='green')
plt.ylabel("Profit", fontsize=14, color='green')
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)
plt.show()

# Profits by Month.
plt.figure(figsize=(10, 5))
sns.scatterplot(x="Month Name", y="Profit", data=finance_sectors, hue="Month Name", palette="viridis",legend=False)
plt.title("Profit by Month", fontsize=16, color="darkblue")
plt.xlabel("Month", fontsize=14, color="green")
plt.ylabel("Profit", fontsize=14, color="green")
plt.xticks(rotation=45)
plt.show()

# **Clustering**

finance_sectors.columns

finance_cluster = finance_sectors[['Units Sold', 'Manufacturing Price', 'Sale Price', 'Gross Sales', 'Discounts', 'COGS', 'Profit']]
finance_cluster

# KMeans Clustering

from sklearn.preprocessing import StandardScaler
ss=StandardScaler()
ss_df=pd.DataFrame(ss.fit_transform(finance_cluster),columns=finance_cluster.columns)
ss_df

from sklearn.cluster import KMeans
km=KMeans(n_clusters=5,random_state=42)
km.fit(ss_df)

set(km.labels_)
finance_cluster["cluster_ID_K"]=km.labels_
finance_cluster

finance_cluster.sort_values(by="cluster_ID_K")

finance_cluster[finance_cluster["cluster_ID_K"]==2]

# Heirarchical Clustering

import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import normalize

finance_cluster_norm=pd.DataFrame(normalize(finance_cluster),columns=finance_cluster.columns)
finance_cluster_norm.head()

fig=plt.figure(figsize=(10,5))
dend=sch.dendrogram(sch.linkage(finance_cluster_norm,"complete"))

ac=AgglomerativeClustering(n_clusters=6,metric="euclidean",linkage="ward")
ac

y=pd.DataFrame(ac.fit_predict(finance_cluster_norm),columns=["cluster_ID_y"])
y["cluster_ID_y"].value_counts()

finance_cluster["cluster_ID_H"]=ac.labels_
finance_cluster.head()

finance_cluster[finance_cluster["cluster_ID_H"]==5].tail()

fig=plt.figure(figsize=(10,5))
plt.scatter(finance_cluster["cluster_ID_H"],finance_cluster["Units Sold"],c=ac.labels_)
