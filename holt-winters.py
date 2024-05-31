#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


# In[2]:


dane = pd.read_excel('Do modelu.xlsx')


# In[3]:


dane


# In[8]:


ho='HIGIENA OSOBISTA'


# In[9]:


ticks=np.sort(dane[ho].index.unique())
w2 = go.Figure(layout =go.Layout(xaxis = dict(ticklabelmode="period", dtick="M1", tickformat="%b\n%",tickvals=list(ticks),
                            ticktext = ticks,linecolor='black',tickwidth=1,tickcolor='black',ticks="outside")))
w2.add_trace(go.Scatter(x=ticks,y=dane[ho]))


# In[10]:


from statsmodels.tsa.seasonal import seasonal_decompose
df1 = dane
df1['miesiac'] = pd.to_datetime(df1['Rok_miesiac'])
df1.set_index(df1.miesiac,inplace=True) #indexy to teraz daty


# In[11]:


decompose_result = seasonal_decompose(df1.loc[:,ho])
decompose_result.plot();


# In[12]:


# time series - statsmodels 
# Seasonality decomposition
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.seasonal import seasonal_decompose 
# holt winters 
# single exponential smoothing
from statsmodels.tsa.holtwinters import SimpleExpSmoothing   
# double and triple exponential smoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing


# In[13]:


hw=df1[['miesiac','HIGIENA OSOBISTA']]
hw=hw.loc[:,['miesiac','HIGIENA OSOBISTA']]
hw


# In[14]:


hw['HWES3'] = ExponentialSmoothing(hw['HIGIENA OSOBISTA'],damped=False,trend='add',seasonal='add',seasonal_periods=12,freq='MS').fit().fittedvalues


# In[15]:


hw


# In[16]:


from sklearn.metrics import mean_absolute_error,mean_squared_error
MSE=mean_squared_error(hw['HIGIENA OSOBISTA'], list(hw['HWES3']))
MAE=mean_absolute_error(hw['HIGIENA OSOBISTA'], list(hw['HWES3']))
RMSE=np.sqrt(MSE)


# In[17]:


MAE


# In[18]:


RMSE


# In[19]:


fighw1 = go.Figure(layout =go.Layout(xaxis = dict(ticklabelmode="period", dtick="M1", tickformat="%b\n%",tickangle=45,tickvals=list(df1['Rok_miesiac'].astype('string')),
                            ticktext = df1['Rok_miesiac'].astype('string'),linecolor='black',tickwidth=1,tickcolor='black',ticks="outside",tickfont=dict(size=12))))
fighw1.add_trace(go.Scatter(
        x = df1['Rok_miesiac'],
        y = hw['HIGIENA OSOBISTA'],
        mode='lines+markers',
        line_color='red'
        ))
fighw1.add_trace(go.Scatter(
    x = df1['Rok_miesiac'],
    y = hw['HWES3'],
    name = "HWES",
    mode='lines+markers',
    marker_size=6,
    line_color = 'dodgerblue',
    opacity = 0.8))
fighw1.update_layout(title='Sprzedaż ilościowa xyz - prognoza')
fighw1.show()


# In[20]:


cz=[]
for i in range(2024,2030): #lata do predykcji
    for j in range(1,13): #miesiace
        if j<=9:
            cz.append(str(i)+'-'+'0'+str(j))
        else:
            cz.append(str(i)+'-'+str(j))       


# In[21]:


fitted_model = ExponentialSmoothing(hw['HIGIENA OSOBISTA'],damped=False,trend='add',seasonal='add',seasonal_periods=12).fit()
test_predictions = fitted_model.forecast(24)


# In[22]:


fig1 = go.Figure(layout =go.Layout(
    xaxis = dict(showgrid=True,tickfont=dict(size=14),title='<b>Data', ticklabelmode="period", dtick="M1", tickformat="%b\n%",tickangle=45,tickvals=cz[:48],
                            ticktext = cz[:48],linecolor='black',tickwidth=1,tickcolor='black',ticks="outside"),
    yaxis = dict(linecolor='black',title='<b>Liczba sprzedaży [w sztukach]',tickwidth=1,tickcolor='black',ticks="outside",gridcolor='black')
    ))
fig1.add_trace(go.Scatter(
        x = cz[:24],
        y = hw['HIGIENA OSOBISTA'],
        name = "xyz",
        line_color = 'red',
        mode='lines+markers',
        marker_size=8,
        line_width=3
        ))  
fig1.add_trace(go.Scatter(
        x = cz[24:],
        y = test_predictions.values,
        name = "HWES_pred",
        mode='lines+markers',
        marker_size=6,
        line_color = 'green',
        opacity = 1))

fig1.update_layout(plot_bgcolor='white',height=550,font=dict(
            size=18,
            color="Black"),title='<b>Prognoza sprzedaży ilościowej kategorii xyz przy urzyciu modelu Holta-Wintersa',title_x=0.5)


# In[ ]:




