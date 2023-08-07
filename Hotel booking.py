#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# In[3]:


df=pd.read_csv('hotel_booking.csv')


# In[4]:


df.head()


# In[5]:


df.tail()


# In[6]:


df.shape


# In[7]:


df.columns


# In[8]:


df.info()


# In[9]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])


# In[10]:


df.info()


# In[11]:


df.describe(include='object')


# In[12]:


for col in df.describe(include='object').columns:
    print(col)
    print(df[col].unique())
    print('-'*50)


# In[13]:


df.isnull().sum()


# In[14]:


df.drop(['company','agent'],axis = 1, inplace = True)
df.dropna(inplace=True)


# In[15]:


df.isnull().sum()


# In[19]:


df.describe()


# In[20]:


df['adr'].plot(kind='box')


# In[18]:


df = df[df['adr']<5000]


# # Data Analysis and Visualization

# In[21]:


cancelled_perc = df['is_canceled'].value_counts(normalize=True)
cancelled_perc


# In[27]:


print(cancelled_perc)
plt.figure(figsize =(5,4))
plt.title('Resevation status count')
plt.bar(['Not cancelled','cancelled'],df['is_canceled'].value_counts(),edgecolor='k',width=0.7)
plt.show()


# The  accompanying bar graph shows the percentage of reservations that aire canceled
# and those that are not. It is obvious  that there are still a significanit number of
# reservations that have not been canceled. There are still 37% of dlients who canceled
# their reservation, which has a significant impact onthe hotels' earmings

# In[34]:


import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 4))
ax1 = sns.countplot(x='hotel', hue='is_canceled', data=df, palette='Blues')
legend_labels, _ = ax1.get_legend_handles_labels()
ax1.legend(legend_labels, ['Not Canceled', 'Canceled'], bbox_to_anchor=(1, 1))
plt.title('Reservation status in different hotels', size=20)
plt.xlabel('hotel')  # Corrected from plt.xlabels() to plt.xlabel()
plt.ylabel('number of reservation')
plt.show()


# In[ ]:


In comparison to resort hotels, city hotels have nore bookings. It's possible that resort
hotels are more expenisive than those in cities.


# In[37]:


resort_hotel = df[df['hotel']=='Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize= True)


# In[38]:


city_hotel = df[df['hotel']=='City Hotel']
city_hotel['is_canceled'].value_counts(normalize= True)


# In[39]:


resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[41]:


plt.figure(figsize=(20,8))
plt.title('Average Daily Rate in city and Resort hotel',fontsize = 30)
plt.plot(resort_hotel.index, resort_hotel['adr'],label = 'Resort Hotel')
plt.plot(city_hotel.index, city_hotel['adr'],label = 'city Hotel')
plt.legend(fontsize = 20)
plt.show()


# The line graph above shows that, on certain days, the average daily rate for a city hotel
# is less than that of a resort hotel, and on other days, it is even less. It goes without
# saying that weekends anid holidays may see a rise in resort hotel rates.

# In[44]:


df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize=(16,8))
ax1 = sns.countplot(x='month',hue = 'is_canceled',data=df,palette='bright')
legend_labels,_ = ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Reservation status per month',size=20)
plt.xlabel('month')
plt.ylabel('number of reservations')
plt.legend(['not canceled','canceld'])
plt.show()


# We have developed the grouped bar graph to analyze the  months with the highest and
# lowest reservation levels according to  reservation status. As can be seen, both the
# number of confirmed reservations and the number of canceled reservations are largest
# in the month of August- whereas January is the month with the most canceled
# reservations

# In[48]:


import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(15, 8))
plt.title('ADR per month', fontsize=30)

# Create the bar plot using barplot()
ax = sns.barplot(x='month', y='adr', data=df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index())

# Add a legend with descriptive labels
ax.legend(labels=['ADR for Canceled Reservations'], fontsize=20)

plt.show()


# This bar graph demonstrates that cancellations are most common when prices  are
# greatest and are  leasit common when they are lowest. Therefore.the  cost of the
# accommodation is solely responsible for the cancellation.
# Now, let's see which couintry has the highest reservation canceled. The top country is
# Portugal with the highest number of cancellatlions.

# In[53]:


canceled_data =  df[df['is_canceled']==1]
top_10_countries = canceled_data['country'].value_counts()[:10]
plt.title('top 10 countries with reservation cancelled')
plt.pie(top_10_countries, autopct = '%.2f',labels= top_10_countries.index)
plt.show()


# This bar graph demonstrates that cancellations are most common when prices  are
# greatest and are  leasit common when they are lowest. Therefore.the  cost of the
# accommodation is solely responsible for the cancellation.
# Now, let's see which couintry has the highest reservation canceled. The top country is
# Portugal with the highest number of cancellatlions.

# In[54]:


df['market_segment'].value_counts()


# In[55]:


df['market_segment'].value_counts(normalize=True)


# In[57]:


canceled_data['market_segment'].value_counts(normalize=True)


# In[60]:


canceled_df_adr = canceled_data.groupby('reservation_status_date')[['adr']].mean()
canceled_df_adr.reset_index(inplace = True)
canceled_df_adr.sort_values('reservation_status_date',inplace=True)

not_canceled_data =  df[df['is_canceled']==0]
not_canceled_df_adr = not_canceled_data.groupby('reservation_status_date')[['adr']].mean()
not_canceled_df_adr.reset_index(inplace = True)
not_canceled_df_adr.sort_values('reservation_status_date',inplace=True)

plt.figure(figsize=(20,6))
plt.title('Aveage Daily Rate')
plt.plot(not_canceled_df_adr['reservation_status_date'],not_canceled_df_adr['adr'],label = 'not canceled')
plt.plot(canceled_df_adr['reservation_status_date'],canceled_df_adr['adr'],label = 'canceled')
plt.legend()


# In[61]:


canceled_df_adr = canceled_df_adr[(canceled_df_adr['reservation_status_date']>'2016')&(canceled_df_adr['reservation_status_date']<'2017-09')]
not_canceled_df_adr = not_canceled_df_adr[(not_canceled_df_adr['reservation_status_date']>'2016')&(not_canceled_df_adr['reservation_status_date']<'2017-09')]



# In[63]:


plt.figure(figsize=(20,6))
plt.title('Aveage Daily Rate',fontsize=30)
plt.plot(not_canceled_df_adr['reservation_status_date'],not_canceled_df_adr['adr'],label = 'not canceled')
plt.plot(canceled_df_adr['reservation_status_date'],canceled_df_adr['adr'],label = 'canceled')
plt.legend()


# As seen in the  graph, reservations are canceled when the average daily rate is higher
# than when it is not canceled. It clearly proves all the above analysis,that the higher
# price leads to higher cancellation.

# Suggestions
# 1. Cancellation rates rise as the price does. In order to prevent cancellations of
# reservations, hotels could work on their pricing  strategies and try to lower the
# rates for specific hoteIs based on locations.
# They can also provide some
# discounts to the consumers
# 2. As the ratio of the cancellation and not cancellation of the resort hotel is higher in
# the resort hotel than the city hotels. So the hotels  should provide a reasonable
# discount on the room prrices on weekends or on holidays.
# 3. In the month of January, hotels can start campaigns or marketing with a
# reasonable amount to increase their revenue as the cancellation is the highest in
# this month.
# They can also increase the quality of their hotels  and their services mainly in
# Portugal to reduce the cancellation rate.
