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








