import pandas as pd
import numpy as np
import warnings
import datetime as dt
warnings.filterwarnings('ignore')
df = pd.read_excel(r'C:\Users\meysam-sadat\Desktop\venus dsh sales statistics\venus dsh data analysis\Final_venusdsh_customers_invoice datasheet\Total_Sales.xls')
df.drop(['price','code','date','qty'],axis=1,inplace=True)
now = dt.datetime(2019,12,30)
df['  date(Gorgian)'] = pd.to_datetime(df['  date(Gorgian)'])
df.rename({'  date(Gorgian)':'date'},axis=1,inplace=True)
df = df[['date','description','customer_name','total']]

rfmtable = df.groupby('customer_name').agg({'date':lambda x:(now - x.max()).days,'description':lambda x: len(x),'total': lambda x:x.sum()})


rfmtable.rename({'date':'recency','description':'frequency','total':'monetary'},axis=1,inplace=True)

quantiles = rfmtable.quantile(q=[0.25,0.5,0.75])

quantiles = quantiles.to_dict()
print(quantiles)

rfmSegmentation = rfmtable

def RClass(x,p,d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]:
        return 3
    else:
        return 4
def FMClass(x,p,d):
    if x <= d[p][0.25]:
        return 4
    elif x <=d[p][0.50]:
        return 3
    elif x <= d[p][0.75]:
        return 2
    else:
        return 1
rfmSegmentation['R_Quartile'] = rfmSegmentation['recency'].apply(RClass,args=('recency',quantiles))
rfmSegmentation['F_Quartile'] = rfmSegmentation['frequency'].apply(FMClass,args=('frequency',quantiles))
rfmSegmentation['M_Quartile'] = rfmSegmentation['monetary'].apply(FMClass,args=('monetary',quantiles))

rfmSegmentation['RFMClass'] = rfmSegmentation.R_Quartile.map(str) \
    + rfmSegmentation.F_Quartile.map(str) \
    + rfmSegmentation.M_Quartile.map(str)
rfmSegmentation = rfmSegmentation.sort_values('RFMClass',ascending=True)
rfmSegmentation['RFMClass'].unique()
rfmSegmentation['RFMClass'] = rfmSegmentation['RFMClass'].astype(str).astype(int)
rfmSegmentation.dtypes


customer_A = rfmSegmentation[(rfmSegmentation['RFMClass'] == 111)]
customer_B = rfmSegmentation[(rfmSegmentation['RFMClass'] == 311)]
customer_c = rfmSegmentation[(rfmSegmentation['RFMClass'] == 211)]
customer_d = rfmSegmentation[(rfmSegmentation['RFMClass'] == 411)]
customer_e = rfmSegmentation[(rfmSegmentation['RFMClass'] == 112)]
customer_f = rfmSegmentation[(rfmSegmentation['RFMClass'] == 121)]
rfmtable_value_counts = rfmSegmentation['RFMClass'].value_counts()


rfmSegmentation.to_excel(r'C:\Users\meysam-sadat\Desktop\venus dsh data analysis\RFM venusdsh.RFM.xlsx')


