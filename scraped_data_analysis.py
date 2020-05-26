# -*- coding: latin-1 -*-
# Analytics on the BeautifulSoup scraped data:
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir('E:\\gitHubProjects\\forGitHub\\beautifulSoup')

#import data:
wdata = pd.read_csv("bookstore_scrape.csv")

#perform data cleanup, basic statistics, maybe clustering?

#raw_data.dtypes                                 *data is good. no missing data
#raw_data.isnull().sum()/len(raw_data)            and all corect dtypes.

wdata.describe()
priceMedian = wdata['PRICE'].median()
ratingMedian = wdata['RATING'].median()


# Histogram:
# price   
plt.figure(figsize=(15,10)) 
sns.distplot(wdata['PRICE'], kde = False, color = 'green',
             hist_kws = {"rwidth": 0.70, 'edgecolor':'gray',
                         'alpha':0.8})
plt.show();

# rating â€”let's use a countplot for this:
plt.figure(figsize=(10,5))
sns.countplot(data=wdata, x='RATING', color='goldenrod')
plt.show();

notes1 = """
notes: 
 - There is a mean price of £35.32, with a standard deviation of 14.34.
 - Minimum price of Â£10.01 and maximum of £59.99, median of £36.26
 - There is a mean rating of 2.897, with a standard deviation of 1.454.
 
"""
#distribution curve per rating:
g = sns.FacetGrid(wdata, row="RATING",
                  height=2.4, aspect=8,)
g.map(sns.distplot, "PRICE", hist=False, rug=True);
plt.close();

notes2 = """ 
notes:
    - as rating increases, we begin to observe a bimodal distribution on the
      book prices. does price influence rating as well? i.e. an 'okay' book
      that is pricedvery cheap could present as a 'great value book' and raise
      its rating
"""
#category vs price:

#g = sns.FacetGrid(wdata, row="CATEGORY",
#                height=2.4, aspect=8,)
#g.map(sns.distplot, "PRICE");

#violin plot: too messy, need to clean up:
#plt.figure(figsize=(30, 20))
#ax = sns.violinplot(x="CATEGORY", y="PRICE", data=wdata)
#plt.show()


notes3="""
notes:
    
    - check book counts first
    
    - nonfiction books are often priced below the median,
      with some slightly more expensive. thse could be
      motivational speaker books.
    
    -  historical books appear with three distinct peaks.
       further analysis should be done on this category.
       you would often think that there should be some correlation with 
       academic category distribution, but there isnt.
       
    - finally, political and cultural books have a bulk of their numbers
      above the median. 
"""

# count of books per category:

wdata['CATEGORY'].unique()

for cat in wdata['CATEGORY'].unique():
    print(cat, len(wdata[wdata["CATEGORY"] == cat]))


notes4 = """
notes:
    - some categories are only represented by one book
"""

#history had 3 distinct peaks, lets look into that:
history_cat_data = wdata[wdata["CATEGORY"] == 'History']


##
# ML price prediction. linear regression (poly)

MLWdata = wdata[['CATEGORY', 'RATING', 'PRICE']]

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split



print(len(wdata)/len(wdata.CATEGORY.unique())) # 10.34 book to cat ratio
                                               # we scale and column transform
                                               
#we want to:
#transform cat via pd get dummies
#split data and separate Y from MOF
#scale MOF

#create target and MOF:
    
X = MLWdata[["RATING"]]
y = MLWdata.iloc[:,-1]

#print(X.shape, y.shape) | (517, 51) (517,)

#transform before scaling:
    
X = pd.get_dummies(X, drop_first=True)

print(X.shape, y.shape)
"""
***dont need?***

#SPLIT:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2,
                                                    random_state = 43)


#split variables are not populating on inspector below

#SCALING:
# Feature Scaling

sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

#print(X_train.shape, X_test.shape) | (413, 50) (104, 50)

"""


#Fitting the polynomial regression:
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree = 2) #*
X_poly = poly_reg.fit_transform(X)

#Fit the created PLR into an MLR:
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_poly, y)

plt.figure(figsize=(15,20))
plt.scatter(X, y, color = 'red')
plt.plot(X, lin_reg_2.predict(poly_reg.fit_transform(X)), color = 'blue')
plt.title("Truth or Bluff? (Polynomial)")
plt.xlabel("Position level")
plt.ylabel("Salary")
plt.show()



#never work with randomized data, it doesn't mean anything.








