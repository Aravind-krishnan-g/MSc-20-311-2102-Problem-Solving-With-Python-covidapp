#!/usr/bin/env python
# coding: utf-8

# In[336]:


import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image 
import requests
import streamlit as st


# In[337]:


class covidapp:
    
    def __init__(self):
        self.df=pd.read_csv(r'https://api.covid19india.org/csv/latest/state_wise_daily.csv') #load covid data
        self.df['Date_YMD']=pd.to_datetime(self.df['Date_YMD'],format='%Y/%m/%d') # convert to datetime objects
        self.df.index=list(self.df['Date_YMD'])
        self.df=self.df.drop(columns=['UN'],axis=0) # drop unnecessary column
        # states names with their respective codes
        self.codes={'India (overall)':'TT','Andaman and Nicobar Islands':'AN','Andhra Pradesh':'AP','Arunachal Pradesh':'AR',
                    'Assam' :'AS','Bihar':'BR','Chandigarh':'CH', 'Chhattisgarh':'CT',
                    'Dadra and Nagar Haveli':'DN','Daman and Diu':'DD','Delhi':'DL','Goa':'GA',
                    'Gujarat':'GJ','Haryana':'HR','Himachal Pradesh':'HP','Jammu and Kashmir':'JK',
                    'Jharkhand':'JH', 'Karnataka':'KA','Kerala':'KL','Ladakh':'LA','Lakshadweep':'LD',
                    'Madhya Pradesh':'MP','Maharashtra':'MH','Manipur':'MN','Meghalaya':'ML','Mizoram':'MZ',
                    'Nagaland':'NL','Orissa':'OR','Pondicherry':'PY','Punjab':'PB','Rajasthan':'RJ',
                    'Sikkim':'SK','Tamil Nadu':'TN','Telangana':'TG','Tripura':'TR','Uttar Pradesh':'UP',
                    'Uttarakhand':'UT','West Bengal':'WB'}
        self.stats=['Confirmed','Recovered','Deceased']
        self.timeframe=['Fetch all data','Monthly data']
        self.months={'January'   : 1, 'February' : 2, 'March'   : 3, 'April'    : 4,
                     'May'       : 5, 'June'     : 6, 'July'    : 7, 'August'   : 8, 
                     'September' : 9, 'October'  :10, 'November':11, 'December' :12}
        
        
    def get_state_data(self,df_old,state,flag=False):
        df_new=df_old[df_old['Status']=='Confirmed'][['Date_YMD','Date',state]].reset_index(drop=True).rename(columns={state:'Confirmed'})
        df_new['Recovered']=df_old[df_old['Status']=='Recovered'][[state]].to_numpy()
        df_new['Deceased'] =df_old[df_old['Status']=='Deceased'][[state]].to_numpy()
        if (flag):
            df_new.reset_index(drop = True,inplace=True)
            df_new.drop(columns=['Date_YMD'],inplace=True)
        else:
            df_new.index=list(df_new['Date_YMD'])
        return df_new
        
    
    
    def data_monthly(self,df_old,month,year):
        condition1 = df_old.index.map(lambda x: x.month) == month
        condition2 = df_old.index.map(lambda x: x.year) == year
        condition = condition1 * condition2
        if condition.sum()==0:
            is_empty=True
        else:
            is_empty=False
        if not is_empty:
            df_new=df_old.iloc[condition]
            df_new.reset_index(drop = True,inplace=True)
            df_new.drop(columns=['Date_YMD'],inplace=True)
            return df_new
        else:
            return None
    
    
    def tab(self,state,df,col):
        col.header("TABULATION")
        col.write(df)
            
    def viz(self,state,df,col,flag):
        if(flag):
            col.header(state) 
        else:
            col.header("VISUALIZATION") 
        #try:
        fig = px.line(df, x='Date', y=self.stats) 
        col.plotly_chart(fig,use_container_width=True)
        #except:
        #    st.error("Error detected. Might be because the data you chose might not be available")
            
    def display(self):
        
        st.title("Covid Data in India")
        st.markdown("## " + 'Data Trends across states')
        my_expander = st.beta_expander("About")
        my_expander.write(""" This web app is made using streamlit library in python. 
            The purpose is to make covid data comprehensible to the common man
            using different tabulations and visualizations.
            """ )
        my_expander.write(" Tabulation is done using pandas data frame and visualization using plotly library.")
        my_expander.write("Plotly charts are interactive. So visual charts, created in this web app, can be interacted with.")
        my_expander.write("You can check out the work at [github](https://github.com/Aravind-krishnan-g/MSc-20-311-2102-Problem-Solving-With-Python-covidapp/tree/main)")
        url1=r'https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/512x512/plain/table.png'
        url2=r'https://makingdatameaningful.com/wp-content/uploads/2018/06/presentation.png'
        image1 = Image.open(requests.get(url1, stream=True).raw)
        image2 = Image.open(requests.get(url2, stream=True).raw)
        col1, col2,  = my_expander.beta_columns(2)
        col2.image(image2, caption='Data visualization',use_column_width=True)
        col1.image(image1, caption='Tabular data',use_column_width=True)
        
        st.sidebar.title(" OPTIONS")   
        region=st.sidebar.selectbox('Select region',list(self.codes.keys()),key='1')
        compare=st.sidebar.checkbox("compare with another state/UT")
        if compare:
            state2=st.sidebar.selectbox('Select state/UT',list(self.codes.keys()),key='2')
        timeline=st.sidebar.selectbox('Select a time frame for fetching data', self.timeframe ,key='3')
        if timeline == 'Fetch all data':
            df1=self.get_state_data(self.df,self.codes[region],True)
            if compare:
                df2=self.get_state_data(self.df,self.codes[state2],True)
        elif timeline == 'Monthly data':
            year_sel=st.sidebar.selectbox("Select year",['2020','2021'],key='5')
            month_sel=st.sidebar.selectbox("Select month",list(self.months.keys()),key='5')
            df0=self.get_state_data(self.df,self.codes[region])
            df1=self.data_monthly(df0,self.months[month_sel],int(year_sel))
            if df1 is None:
                st.warning("Data not available!!!")
            if compare:
                df0=self.get_state_data(self.df,self.codes[state2],False)
                df2=self.data_monthly(df0,self.months[month_sel],int(year_sel))
                if df2 is None:
                    st.warning("Data not available!!!")
          
                
        if compare:
            mode=st.sidebar.selectbox('Select mode of presentation',['Visualization'],key='4')
            if st.sidebar.button("Show data"):
                col1=st.beta_container()
                self.viz(region,df1,col1,True) 
                col2=st.beta_container()               
                self.viz(state2,df2,col2,True)     
        else:
            mode=st.sidebar.selectbox('Select mode of presentation',['Tabulation','Visualization','Show both'],key='5')
            if st.sidebar.button("Show data"):
                if mode == 'Visualization':
                    col1=st.beta_container()
                    self.viz(region,df1,col1,True) 
                
                if mode == 'Tabulation':
                    col2=st.beta_container()
                    self.tab(region,df1,col2)
                    
                if mode == 'Show both':
                    st.write("State selected :",region)
                    col3=st.beta_container()
                    self.viz(region,df1,col3,False) 
                    col4=st.beta_container()  
                    self.tab(region,df1,col4)
            
            
                


# ## DRIVER CODE

# In[340]:


class_obj=covidapp()
class_obj.display()

