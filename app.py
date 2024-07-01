
import matplotlib.pyplot as plt
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
st.pyplot(df.groupby('type')['price'].mean().plot(kind='bar'))

st.markdown("The bar graph shows a comparison between the types of vehicles offered and the list price. Truck is the type of vehicle with the highest price, exceeding 200 million. SUV and Pickup also have high prices, but not as much as Trucks. Most other vehicle types (Coupe, Van, Convertible, Hatchback, Wagon, Mini-Van, Other, Offroad, Bus) have considerably lower prices, usually below 50 million. Bus is the type of vehicle with the lowest price. Conclusion: There is great variability in the prices of different types of vehicles. Trucks dominate in terms of price, followed by SUVs and Pickups. Many other types of vehicles have relatively low prices compared to Trucks, SUVs, and Pickups.")


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
