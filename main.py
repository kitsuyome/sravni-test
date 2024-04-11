import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
@st.cache
def load_data():
    data = pd.read_csv('/path/to/your/data.csv', encoding='ISO-8859-1')
    # Преобразование строки InvoiceDate в datetime
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    return data

data = load_data()

# Заголовок приложения
st.title('Анализ данных о продажах')

# Выбор диапазона дат
date_range = st.date_input('Выберите диапазон дат', [])
if date_range:
    start_date, end_date = date_range
    mask = (data['InvoiceDate'].dt.date >= start_date) & (data['InvoiceDate'].dt.date <= end_date)
    filtered_data = data.loc[mask]
else:
    filtered_data = data

# Отображение ключевых метрик
st.write('Ключевые метрики:')
st.write(f"- Общее количество продаж: {filtered_data['Quantity'].sum()}")
st.write(f"- Количество уникальных клиентов: {filtered_data['CustomerID'].nunique()}")
st.write(f"- Количество уникальных счетов-фактур: {filtered_data['InvoiceNo'].nunique()}")

# Визуализация продаж по странам
country_sales = filtered_data.groupby('Country')['Quantity'].sum().sort_values(ascending=False)
st.bar_chart(country_sales)

# Визуализация динамики продаж
filtered_data['Date'] = filtered_data['InvoiceDate'].dt.date
sales_over_time = filtered_data.groupby('Date')['Quantity'].sum()
st.line_chart(sales_over_time)
