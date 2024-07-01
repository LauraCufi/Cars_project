import streamlit as st
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
import pyarrow as pa


df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

st.header('Car advertisement dataset')
st.markdown("Continuing, a project corresponding to Sprint 4 of TripleTen's Dat Science program was released. This project analyzes different factors from the data base of a vehicle owner and shows the conclusions of drawing graphics and analyzing data")
st.markdown("The sidebar offers the option to filter the total data, by year, model and condition. Upon selection the data table will be updated with the selected data. Below is an analysis of the condition of the vehicle compared to the price, the types of vehicles in relation to the manufacturer and a price comparison between the selected manufacturers.")
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

st.header("Type vs price")
#st.pyplot(df.groupby('type')['price'].mean().plot(kind='bar'))
mean_prices = df.groupby('type')['price'].mean().reset_index()
st.write(px.bar(mean_prices, x='type', y='price'))




st.markdown("Buses and trucks are the most expensive, reaching prices of approximately 16,000. Convertibles and coupes also have high prices, around 15,000. Hatchbacks and sedans are more economical, with prices around 7,000 and 9,000 respectively. SUVs, pickup trucks, and offroad vehicles are in a medium to high price range. This analysis suggests that the type of vehicle significantly influences its price, with larger and more specialized vehicles tending to cost more.")

st.header('Vehicle types by manufacturer')
st.write(px.histogram(df, x='manufacturer', color='type'))

st.markdown('In the vehicle type graph vs the manufacturer, compare the different manufacturers offered and the types of vehicles available between those that are shown: suv, sedam, cup, cupe, among others. From the graphics we can conclude that the manufacturer has the majority of offers available in a variety of vehicle types such as Ford. The manufacturer with a small variety of Mercedes-Benz vehicles only offers “van” type vehicles.')

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
