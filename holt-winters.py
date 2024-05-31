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
t = col1.selectbox('Wybierz rodzaj trendu  :',['addytywny','multiplikatywny'])
s = col2.selectbox('Wybierz rodzaj sezonowości  :',['addytywny','multiplikatywny'])
sz = col3.selectbox('Czy stłumić składnik trendu:',['tak','nie'])





