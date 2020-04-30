# -*- coding: latin-1 -*-
# Analytics on the BeautifulSoup scraped data:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
sns.distplot(wdata['PRICE'], kde = False, color = 'green',
             hist_kws = {"rwidth": 0.70, 'edgecolor':'gray',
                         'alpha':0.8})
plt.show();

# rating —let's use a countplot for this:
sns.countplot(data=wdata, x='RATING', color='goldenrod')
plt.show();

notes = """
notes: 
 - There is a mean price of £35.32, with a standard deviation of 14.34.
 - Minimum price of £10.01 and maximum of £59.99, median of £36.26
 - There is a mean rating of 2.897, with a standard deviation of 1.454.
 
"""

#TODO: analyze prices per rating value.