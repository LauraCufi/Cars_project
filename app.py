import streamlit as st
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
import pyarrow as pa

df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

st.header('Car advertisement dataset')
st.markdown("In this project, the data of a car dealer will be analyzed")
st.sidebar.header("User input features")


sorted_unique_year=sorted(df.model_year.unique())
selected_year=st.sidebar.multiselect('Year', list(reversed(range(1999,2014))))

sorted_unique_model=sorted(df.model.unique())
selected_model=st.sidebar.multiselect('Model year',sorted_unique_model,sorted_unique_model)

unique_condition=['excellent','fair','good','like new','new','salvage']
selected_contidion=st.sidebar.multiselect('Condition',unique_condition,unique_condition)

df_selected_model=df[(df.model_year.isin(selected_year)) & (df.model.isin(selected_model)) & (df.condition.isin(selected_contidion))]

st.header("Display model and contion cars")
st.write("Data Dimension: "+ str (df_selected_model.shape[0])+"rows and "+str(df_selected_model.shape[1]) + ' columns.')
st.dataframe(df_selected_model)

st.header('Condition vs price')
st.write(px.histogram(df, x='condition', color='price'))




st.header('Vehicle types by manufacturer')
st.write(px.histogram(df, x='manufacturer', color='type'))



st.header('Compare price distribution between manufacturers')
manufac_list = sorted(df['manufacturer'].unique())
manufacturer_1 = st.selectbox('Select manufacturer 1',
                              manufac_list, index=manufac_list.index('chevrolet'))

manufacturer_2 = st.selectbox('Select manufacturer 2',
                              manufac_list, index=manufac_list.index('hyundai'))
mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
st.write(px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay'))
