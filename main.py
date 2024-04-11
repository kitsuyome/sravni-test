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
    data['Date'] = data['InvoiceDate'].dt.date
    data['Week'] = data['InvoiceDate'].dt.isocalendar().week
    data['Month'] = data['InvoiceDate'].dt.month
    data['Year'] = data['InvoiceDate'].dt.year
    return data

data = load_data()

# Установка выбора дат по умолчанию
default_start_date = data['InvoiceDate'].min().date()
default_end_date = data['InvoiceDate'].max().date()

# Функция для рисования графиков
def plot_metric(df, title, x_label, y_label, hover_name):
    fig = px.line(df, x=x_label, y=y_label, title=title, labels={y_label: hover_name})
    fig.update_layout(xaxis_title=x_label, yaxis_title=hover_name)
    st.plotly_chart(fig, use_container_width=True)

# Создание страниц
st.sidebar.title("Метрики")
page = st.sidebar.radio("Выберите период", ('Дневные метрики', 'Недельные метрики', 'Месячные метрики'))

date_range = st.sidebar.date_input('Выберите диапазон дат', [default_start_date, default_end_date])
start_date, end_date = date_range
mask = (data['InvoiceDate'].dt.date >= start_date) & (data['InvoiceDate'].dt.date <= end_date)
filtered_data = data.loc[mask]

if page == 'Дневные метрики':
    st.title('Дневные метрики')
    dau_data = filtered_data.groupby('Date')['CustomerID'].nunique().reset_index(name='Unique Customers')
    plot_metric(dau_data, 'Daily Active Users (DAU)', 'Date', 'Unique Customers', 'Unique Customers')
    sales_data = filtered_data.groupby('Date')['Quantity'].sum().reset_index(name='Total Sales')
    plot_metric(sales_data, 'Daily Sales', 'Date', 'Total Sales', 'Total Sales')
    revenue_data = filtered_data.groupby('Date')['Revenue'].sum().reset_index(name='Total Revenue')
    plot_metric(revenue_data, 'Daily Revenue', 'Date', 'Total Revenue', 'Total Revenue')
elif page == 'Недельные метрики':
    st.title('Недельные метрики')
    wau_data = filtered_data.groupby(['Year', 'Week'])['CustomerID'].nunique().reset_index(name='Unique Customers')
    plot_metric(wau_data, 'Weekly Active Users (WAU)', 'Week', 'Unique Customers', 'Unique Customers')
    sales_data = filtered_data.groupby(['Year', 'Week'])['Quantity'].sum().reset_index(name='Total Sales')
    plot_metric(sales_data, 'Weekly Sales', 'Week', 'Total Sales', 'Total Sales')
    revenue_data = filtered_data.groupby(['Year', 'Week'])['Revenue'].sum().reset_index(name='Total Revenue')
    plot_metric(revenue_data, 'Weekly Revenue', 'Week', 'Total Revenue', 'Total Revenue')
elif page == 'Месячные метрики':
    st.title('Месячные метрики')
    mau_data = filtered_data.groupby(['Year', 'Month'])['CustomerID'].nunique().reset_index(name='Unique Customers')
    plot_metric(mau_data, 'Monthly Active Users (MAU)', 'Month', 'Unique Customers', 'Unique Customers')
    sales_data = filtered_data.groupby(['Year', 'Month'])['Quantity'].sum().reset_index(name='Total Sales')
    plot_metric(sales_data, 'Monthly Sales', 'Month', 'Total Sales', 'Total Sales')
    revenue_data = filtered_data.groupby(['Year', 'Month'])['Revenue'].sum().reset_index(name='Total Revenue')
    plot_metric(revenue_data, 'Monthly Revenue', 'Month', 'Total Revenue', 'Total Revenue')
