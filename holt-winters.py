#!/usr/bin/env python
# coding: utf-8

# In[1]:

import streamlit as st
import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

dane = pd.read_excel('Do modelu.xlsx')

st.header('Model Holt-Winters')
st.subheader('Model Holta-Wintersa, nazywany również modeliem wygładzania wykładniczego, jest jednym z najpopularniejszych modeli do prognozowania danych szeregów czasowych. Model ten jest szczególnie skuteczny przy prognozowaniu danych, które wykazują zarówno sezonowość, jak i trend.')
ll, rr = st.columns((2,2))



kategorie=dane.columns
kategorie=kategorie[2:]

wybor_kat = st.selectbox('Wybierz kategorię :', kategorie)

st.subheader('Wybierz parametry modelu :')
col1, col2, col3= st.columns(3)
t = col1.selectbox('Wybierz rodzaj trendu  :',['Addytywny','Multiplikatywny'])
s = col2.selectbox('Wybierz rodzaj sezonowości  :',['Addytywny','Multiplikatywny'])
sz = col3.selectbox('Czy stłumić składnik trendu:',['Tak','Nie'])

if t=='Addytywny':
  wybor_t='add'
else:
  wybor_t='mul'
if s=='Addytywny':
  wybor_s='add'
else:
  wybor_s='mul'
if sz=='Tak':
  wybor_sz=True
else:
  wybor_sz=False



from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.seasonal import seasonal_decompose 
from statsmodels.tsa.holtwinters import SimpleExpSmoothing   
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# model
df1 = dane
df1['miesiac'] = pd.to_datetime(df1['Rok_miesiac'])
df1.set_index(df1.miesiac,inplace=True) #indexy to teraz daty

hw=df1[['miesiac',wybor_kat]]
hw=hw.loc[:,['miesiac',wybor_kat]]

hw['HWES3'] = ExponentialSmoothing(hw[wybor_kat],damped=wybor_sz,trend=wybor_t,seasonal=wybor_s,seasonal_periods=12,freq='MS').fit().fittedvalues

from sklearn.metrics import mean_absolute_error,mean_squared_error
MSE=mean_squared_error(hw[wybor_kat], list(hw['HWES3']))
MAE=mean_absolute_error(hw[wybor_kat], list(hw['HWES3']))
RMSE=np.sqrt(MSE)

#wizualizacja
fighw1 = go.Figure(layout =go.Layout(xaxis = dict(ticklabelmode="period", dtick="M1", tickformat="%b\n%",tickangle=90,tickvals=list(df1['Rok_miesiac'].astype('string')),
                            ticktext = df1['Rok_miesiac'].astype('string'),linecolor='black',tickwidth=2,tickcolor='black',ticks="outside",tickfont=dict(size=12))))
fighw1.add_trace(go.Scatter(
        x = df1['Rok_miesiac'],
        y = hw[wybor_kat],
        mode='lines+markers',
        line_color='coral'
        name='Neuca',
        ))
fighw1.add_trace(go.Scatter(
    x = df1['Rok_miesiac'],
    y = hw['HWES3'],
    name = "Holt-Winters",
    mode='lines+markers',
    marker_size=6,
    line_color = 'aquamarine',)
fighw1.update_layout(title=f'Ilościowa sprzedaż kategorii {wybor_kat.lower()} w Neuce w podziale na miesiące')
fighw1.show()

st.plotly_chart(fighw1,True)

cz=[]
for i in range(2024,2030): #lata do predykcji
    for j in range(1,13): #miesiace
        if j<=9:
            cz.append(str(i)+'-'+'0'+str(j))
        else:
            cz.append(str(i)+'-'+str(j))       



fitted_model = ExponentialSmoothing(hw[wybor_kat],damped=wybor_sz,trend=wybor_t,seasonal=wybor_s,seasonal_periods=12).fit()
test_predictions = fitted_model.forecast(24)

fighw2 = go.Figure(layout =go.Layout(
    xaxis = dict(tickfont=dict(size=14),title='<b>Data', ticklabelmode="period", dtick="M1", tickformat="%b\n%",tickangle=90,tickvals=cz[:48],
                            ticktext = cz[:48],linecolor='black',tickwidth=1,tickcolor='black',ticks="outside"),
    yaxis = dict(linecolor='black',title='<b>Liczba sprzedaży [w sztukach]',tickwidth=1,tickcolor='black',ticks="outside",gridcolor='black')
    ))
fighw2.add_trace(go.Scatter(
        x = cz[:24],
        y = hw[wybor_kat],
        name = "xyz",
        line_color = 'red',
        mode='lines+markers',
        marker_size=8,
        line_width=3
        ))  
fighw2.add_trace(go.Scatter(
        x = cz[24:],
        y = test_predictions.values,
        name = "HWES_pred",
        mode='lines+markers',
        marker_size=6,
        line_color = 'green',
        opacity = 1))

fighw2.update_layout(plot_bgcolor='white',height=550,font=dict(
            size=18,
            color="Black"),title='<b>Prognoza sprzedaży ilościowej kategorii xyz przy urzyciu modelu Holta-Wintersa',title_x=0.5)


st.plotly_chart(fighw2,True)
