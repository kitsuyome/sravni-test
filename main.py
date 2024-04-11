import streamlit as st
import pandas as pd
import plotly.express as px
from plotly import graph_objs as go

# Загрузка и кэширование данных
@st.cache
def load_data():
    data = pd.read_csv('data.csv', encoding='ISO-8859-1')
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    data['Revenue'] = data['Quantity'] * data['UnitPrice']
    return data

data = load_data()

# Заголовок приложения
st.title('Аналитика продаж')

# Установка выбора дат по умолчанию от минимальной до максимальной
default_start_date = data['InvoiceDate'].min().date()
default_end_date = data['InvoiceDate'].max().date()
date_range = st.date_input('Выберите диапазон дат', [default_start_date, default_end_date])

start_date, end_date = date_range
mask = (data['InvoiceDate'].dt.date >= start_date) & (data['InvoiceDate'].dt.date <= end_date)
filtered_data = data.loc[mask]

# Расчет DAU, WAU, MAU
filtered_data['Date'] = filtered_data['InvoiceDate'].dt.date
filtered_data['Week'] = filtered_data['InvoiceDate'].dt.isocalendar().week
filtered_data['Month'] = filtered_data['InvoiceDate'].dt.month
filtered_data['Year'] = filtered_data['InvoiceDate'].dt.year

# Функция для отображения графика активности
def plot_activity(df, title, time_col='Date'):
    activity = df.groupby([time_col])['CustomerID'].nunique().reset_index()
    fig = px.line(activity, x=time_col, y='CustomerID', title=title)
    st.plotly_chart(fig, use_container_width=True)

plot_activity(filtered_data, 'Daily Active Users (DAU)', 'Date')
plot_activity(filtered_data, 'Weekly Active Users (WAU)', 'Week')
plot_activity(filtered_data, 'Monthly Active Users (MAU)', 'Month')

# Расчет и визуализация продаж и прибыли
def plot_sales_and_revenue(df, time_col='Date'):
    sales = df.groupby([time_col])['Quantity'].sum().reset_index()
    revenue = df.groupby([time_col])['Revenue'].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sales[time_col], y=sales['Quantity'], mode='lines', name='Sales'))
    fig.add_trace(go.Scatter(x=revenue[time_col], y=revenue['Revenue'], mode='lines', name='Revenue'))
    fig.update_layout(title='Sales & Revenue Over Time', xaxis_title='Time', yaxis_title='Amount')
    st.plotly_chart(fig, use_container_width=True)

plot_sales_and_revenue(filtered_data)

# Визуализация ARPPU
def plot_arppu(df):
    arppu_data = df.groupby('Date').apply(lambda x: x['Revenue'].sum() / x['CustomerID'].nunique()).reset_index(name='ARPPU')
    fig = px.line(arppu_data, x='Date', y='ARPPU', title='ARPPU Over Time')
    st.plotly_chart(fig, use_container_width=True)

plot_arppu(filtered_data)
