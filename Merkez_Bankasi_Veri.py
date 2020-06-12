# -*- coding: utf-8 -*-
"""
Created on Sun May 10 14:29:23 2020

@author: Faruk.Buldur
"""
#%%

# Using Central Bank Data
API_KEY = '07qjI0Sk0l'

# Importing Necessary Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from datetime import date
from tabulate import tabulate

#%%

# Accesing the lists of DataGroups in Central Bank
master_data = pd.read_csv("https://evds2.tcmb.gov.tr/service/evds/datagroups/\
key="+API_KEY+"&mode=0&type=csv")
master_data.head()

#%%

# Accesing Currency DataGroup in Central Bank
curr_data = pd.read_csv("https://evds2.tcmb.gov.tr/service/evds/serieList/\
key="+API_KEY+"&type=csv&code=bie_dkdovytl")

curr_data.drop(["DATASOURCE_ENG","METADATA_LINK","REV_POL_LINK_ENG",
        "APP_CHA_LINK_ENG","TAG_ENG","METADATA_LINK_ENG","DEFAULT_AGG_METHOD_STR",
        "TAG","REV_POL_LINK","APP_CHA_LINK","DEFAULT_AGG_METHOD"], axis=1,inplace=True)
                       
# Accessing to a specific currency in Central Bank.

print(tabulate(curr_data, headers='keys', tablefmt='psql'))

#%%
currency_index = int(input("Please enter the index of currency from above list: "))

series =curr_data.loc[currency_index,"SERIE_CODE"]
series_name=curr_data.loc[currency_index,"SERIE_NAME"]

#Central Bank Format
startDate= "01-01-%202019"
endDate="10-05-%202020"
typee="csv"
key=API_KEY
aggregationTypes="avg"
formulas="0"
frequency = "1"

url= 'https://evds2.tcmb.gov.tr/service/evds/series={}&startDate={}&endDate={}&type={}&\
key={}&aggregationTypes={}&formulas={}&frequency={}'.format(series,startDate,\
endDate,typee,key,aggregationTypes,formulas,frequency)
#%%
# Reading Requested Currency to a DataFrame
requested_curr = pd.read_csv(url)

# Some initial pre-processing
requested_curr.drop("UNIXTIME", axis=1,inplace=True)
requested_curr.rename(columns={series.replace(".","_"):series_name},inplace=True)
requested_curr.tail()

Days_Of_Week_Dict ={0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',
					5:'Saturday',6:'Sunday'}

Days_Of_Week = pd.Series(index=range(len(requested_curr.index)),name='Days Of Week',dtype=int)

requested_curr=pd.concat([requested_curr,Days_Of_Week],axis=1)

for i in range(len(requested_curr.index)):	
	requested_curr['Days Of Week'][i]=datetime.strptime(requested_curr['Tarih'][i], '%d-%m-%Y').date().weekday()

requested_curr['Days Of Week'] = requested_curr['Days Of Week'].map(Days_Of_Week_Dict)

requested_curr_wo_NA=requested_curr.dropna()

requested_curr_wo_NA.set_index("Tarih",inplace=True)

requested_curr_wo_NA


requested_curr_wo_NA[requested_curr_wo_NA.columns[0]].plot()
plt.show()