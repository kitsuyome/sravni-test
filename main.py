import streamlit as st
import pandas as pd
import plotly.express as px
from plotly import graph_objs as go

# Загрузка и кэширование данных
def load_data():
    data = pd.read_csv('/sravni-test/data.csv', encoding='ISO-8859-1')
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    return data

data = load_data()

# Заголовок приложения
st.title('Аналитика продаж')

# Выбор диапазона дат
date_range = st.date_input('Выберите диапазон дат', [])
if date_range:
    start_date, end_date = date_range
    mask = (data['InvoiceDate'].dt.date >= start_date) & (data['InvoiceDate'].dt.date <= end_date)
    filtered_data = data.loc[mask]
else:
    filtered_data = data

# Расчет и отображение DAU, WAU, MAU
filtered_data['Date'] = filtered_data['InvoiceDate'].dt.date
filtered_data['Week'] = filtered_data['InvoiceDate'].dt.isocalendar().week
filtered_data['Month'] = filtered_data['InvoiceDate'].dt.month

DAU = filtered_data.groupby('Date')['CustomerID'].nunique()
WAU = filtered_data.groupby('Week')['CustomerID'].nunique()
MAU = filtered_data.groupby('Month')['CustomerID'].nunique()

st.write('DAU, WAU, MAU по пользователям:')
st.write(f"- DAU: {DAU.mean():.2f}")
st.write(f"- WAU: {WAU.mean():.2f}")
st.write(f"- MAU: {MAU.mean():.2f}")

# Расчет и отображение Daily, Weekly, and Monthly Sales
Daily_Sales = filtered_data.groupby('Date')['Quantity'].sum()
Weekly_Sales = filtered_data.groupby('Week')['Quantity'].sum()
Monthly_Sales = filtered_data.groupby('Month')['Quantity'].sum()

# Визуализация продаж по странам
country_sales = filtered_data.groupby('Country')['Quantity'].sum().sort_values(ascending=False)
fig_country_sales = px.bar(x=country_sales.index, y=country_sales.values, labels={'x':'Country', 'y':'Sales'})
st.plotly_chart(fig_country_sales, use_container_width=True)

# Визуализация динамики продаж
fig_sales_over_time = go.Figure()
fig_sales_over_time.add_trace(go.Scatter(x=Daily_Sales.index, y=Daily_Sales.values, mode='lines', name='Daily Sales'))
fig_sales_over_time.add_trace(go.Scatter(x=Weekly_Sales.index, y=Weekly_Sales.values, mode='lines', name='Weekly Sales'))
fig_sales_over_time.add_trace(go.Scatter(x=Monthly_Sales.index, y=Monthly_Sales.values, mode='lines', name='Monthly Sales'))
fig_sales_over_time.update_layout(title='Sales Over Time', xaxis_title='Time', yaxis_title='Sales')
st.plotly_chart(fig_sales_over_time, use_container_width=True)
