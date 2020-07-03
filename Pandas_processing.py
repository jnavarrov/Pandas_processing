
# coding: utf-8

# Version 1.0.3

# # Pandas basics 

# Hi! In this programming assignment you need to refresh your `pandas` knowledge. You will need to do several [`groupby`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.groupby.html)s and [`join`]()`s to solve the task. 

# In[2]:


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

from grader import Grader


# In[3]:


DATA_FOLDER = '../readonly/final_project_data/'

transactions    = pd.read_csv(os.path.join(DATA_FOLDER, 'sales_train.csv.gz'))
items           = pd.read_csv(os.path.join(DATA_FOLDER, 'items.csv'))
item_categories = pd.read_csv(os.path.join(DATA_FOLDER, 'item_categories.csv'))
shops           = pd.read_csv(os.path.join(DATA_FOLDER, 'shops.csv'))


# The dataset we are going to use is taken from the competition, that serves as the final project for this course. You can find complete data description at the [competition web page](https://www.kaggle.com/c/competitive-data-science-final-project/data). To join the competition use [this link](https://www.kaggle.com/t/1ea93815dca248e99221df42ebde3540).

# ## Grading

# We will create a grader instace below and use it to collect your answers. When function `submit_tag` is called, grader will store your answer *locally*. The answers will *not* be submited to the platform immediately so you can call `submit_tag` function as many times as you need. 
# 
# When you are ready to push your answers to the platform you should fill your credentials and run `submit` function in the <a href="#Authorization-&-Submission">last paragraph</a>  of the assignment.

# In[4]:


grader = Grader()


# # Task

# Let's start with a simple task. 
# 
# <ol start="0">
#   <li><b>Print the shape of the loaded dataframes and use [`df.head`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.head.html) function to print several rows. Examine the features you are given.</b></li>
# </ol>

# In[5]:


transactions.head()


# In[6]:


transactions['date'].dtype


# In[7]:


# Question 1.
# GROUP BY DATE:
transactions['date'] = pd.to_datetime(transactions['date'], format= '%d.%m.%Y')


# In[8]:


transactions['date'].dtype


# In[9]:


import pandas as pd
from datetime import date

date_from = pd.Timestamp(date(2014,9,1))
date_to = pd.Timestamp(date(2014,9,30))

transactions2 = transactions[
    (transactions['date'] >= date_from ) &
    (transactions['date'] <= date_to)
]
transactions2


# Now use your `pandas` skills to get answers for the following questions. 
# The first question is:
# 
# 1. ** What was the maximum total revenue among all the shops in September, 2014?** 
# 
# 
# * Hereinafter *revenue* refers to total sales minus value of goods returned.
# 
# *Hints:*
# 
# * Sometimes items are returned, find such examples in the dataset. 
# * It is handy to split `date` field into [`day`, `month`, `year`] components and use `df.year == 14` and `df.month == 9` in order to select target subset of dates.
# * You may work with `date` feature as with strings, or you may first convert it to `pd.datetime` type with `pd.to_datetime` function, but do not forget to set correct `format` argument.

# In[10]:


# CALCULATING THE REVENUE AND ADDING IT TO TRANSACTIONS DF
transactions2['revenue'] = transactions2.item_price * transactions2.item_cnt_day


# In[11]:


tg = transactions2.groupby('shop_id')
tg.first()


# In[12]:


#ADDING UP  THE REVENUE
Total = tg['revenue'].sum().max()
print (Total)


# In[13]:


max_revenue = 7982852.2 # PUT YOUR ANSWER IN THIS VARIABLE
grader.submit_tag('max_revenue', max_revenue)


# In[14]:


# Question 2 -------------------------------------------
# Get transactions for months 6, 7, 8 in 2014. Once again make revenue column. Groupby item_id, sum the revenues and get item_id of max revenue.
import pandas as pd
from datetime import date

date_from = pd.Timestamp(date(2014,6,1))
date_to = pd.Timestamp(date(2014,8,31))

transactions_summer = transactions[
    (transactions['date'] >= date_from ) &
    (transactions['date'] <= date_to)
]
transactions_summer


# In[15]:


items.head(5)


# In[16]:


transactions_summer['revenue2'] = transactions_summer.item_price * transactions_summer.item_cnt_day


# In[17]:


transactions_summer


# In[18]:


merged_transactions = pd.merge(items, transactions_summer, on='item_id')


# In[19]:


merged_transactions


# In[20]:


by_cat = merged_transactions.groupby(['item_category_id'])
by_cat.first()


# In[21]:


sum_by_cat = by_cat.sum()


# In[22]:


cat_id_max_rev_idx = sum_by_cat['revenue2'].argmax()
print(cat_id_max_rev_idx)


# Great! Let's move on and answer another question:
# 
# <ol start="2">
#   <li><b>What item category generated the highest revenue in summer 2014?</b></li>
# </ol>
# 
# * Submit `id` of the category found.
#     
# * Here we call "summer" the period from June to August.
# 
# *Hints:*
# 
# * Note, that for an object `x` of type `pd.Series`: `x.argmax()` returns **index** of the maximum element. `pd.Series` can have non-trivial index (not `[1, 2, 3, ... ]`).

# In[23]:


# YOUR CODE GOES HERE

category_id_with_max_revenue = 12,6675 # PUT YOUR ANSWER IN THIS VARIABLE
grader.submit_tag('category_id_with_max_revenue', category_id_with_max_revenue)


# <ol start="3">
#   <li><b>How many items are there, such that their price stays constant (to the best of our knowledge) during the whole period of time?</b></li>
# </ol>
# 
# * Let's assume, that the items are returned for the same price as they had been sold.

# In[24]:


# YOUR CODE GOES HERE
# Question 3 ----------------------------------------------------------------
counts = transactions.groupby('item_id')['item_price'].nunique()

num_items_constant_price = counts.value_counts().loc[1]
num_items_constant_price

num_items_constant_price = 5926 # PUT YOUR ANSWER IN THIS VARIABLE
grader.submit_tag('num_items_constant_price', num_items_constant_price)


# In[25]:


# QUESTION 4 ------------------------------------------------------------

date_from = pd.Timestamp(date(2014,12,1))
date_to = pd.Timestamp(date(2014,12,31))

transactions_25 = transactions[
    (transactions['date'] >= date_from ) &
    (transactions['date'] <= date_to)
]
transactions_25


# In[26]:


transactions_25 = transactions_25[transactions_25['shop_id'] == 25]
transactions_25


# In[27]:


transactions_25['day'] = transactions_25.date.dt.day
transactions_25


# In[28]:


transactions_25_grouped = transactions_25.groupby('date')
transactions_25_grouped.first()


# Remember, the data can sometimes be noisy.

# <ol start="4">
#   <li><b>What was the variance of the number of sold items per day sequence for the shop with `shop_id = 25` in December, 2014? Do not count the items, that were sold but returned back later.</b></li>
# </ol>
# 
# * Fill `total_num_items_sold` and `days` arrays, and plot the sequence with the code below.
# * Then compute variance. Remember, there can be differences in how you normalize variance (biased or unbiased estimate, see [link](https://math.stackexchange.com/questions/496627/the-difference-between-unbiased-biased-estimator-variance)). Compute ***unbiased*** estimate (use the right value for `ddof` argument in `pd.var` or `np.var`). 
# * If there were no sales at a given day, ***do not*** impute missing value with zero, just ignore that day

# In[29]:


shop_id = 25

total_num_items_sold =  transactions_25_grouped.item_cnt_day.sum() # YOUR CODE GOES HERE
days = transactions_25_grouped.day.unique() # YOUR CODE GOES HERE

# Plot it
plt.plot(days, total_num_items_sold)
plt.ylabel('Num items')
plt.xlabel('Day')
plt.title("Daily revenue for shop_id = 25")
plt.show()

total_num_items_sold_var =  (np.var(total_num_items_sold , ddof=1)) # PUT YOUR ANSWER IN THIS VARIABLE
grader.submit_tag('total_num_items_sold_var', total_num_items_sold_var)


# ## Authorization & Submission
# To submit assignment to Cousera platform, please, enter your e-mail and token into the variables below. You can generate token on the programming assignment page. *Note:* Token expires 30 minutes after generation.

# In[30]:


STUDENT_EMAIL = 'diegonavarroflorez@gmail.com'
STUDENT_TOKEN = '179cwzbtw2GIgrrx'
grader.status()


# In[32]:


grader.submit(STUDENT_EMAIL, STUDENT_TOKEN)


# Well done! :)
