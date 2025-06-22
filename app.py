import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="📊 Dashboard Supply Chain", layout="wide")
st.title("📦 Analisis Risiko Keterlambatan Pengiriman")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("DataCoSupplyChainDataset.csv", encoding="latin1")

df = load_data()

# Filter kolom yang relevan
dt = df[['Shipping Mode',
         'Days for shipment (scheduled)',
         'Order Item Quantity',
         'Order Item Product Price',
         'order date (DateOrders)',
         'Order Item Discount',
         'Order Item Discount Rate',
         'Order Item Profit Ratio',
         'Sales',
         'Customer Segment',
         'Order Region',
         'Order Item Total',
         'shipping date (DateOrders)',
         'Late_delivery_risk']]

# Date Convert
dt['order date (DateOrders)'] = pd.to_datetime(dt['order date (DateOrders)'])
dt['shipping date (DateOrders)'] = pd.to_datetime(dt['shipping date (DateOrders)'])

# Sidebar filter
with st.sidebar:
    st.header("📌 Filter Data")
    region = st.multiselect("Pilih Region", options=dt['Order Region'].unique(), default=None)
    mode = st.multiselect("Pilih Shipping Mode", options=dt['Shipping Mode'].unique(), default=None)
    segment = st.multiselect("Pilih Customer Segment", options=dt['Customer Segment'].unique(), default=None)

# Terapkan filter jika ada
if region:
    dt = dt[dt['Order Region'].isin(region)]
if mode:
    dt = dt[dt['Shipping Mode'].isin(mode)]
if segment:
    dt = dt[dt['Customer Segment'].isin(segment)]

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📦 Total Order", len(dt))
with col2:
    late_pct = dt['Late_delivery_risk'].mean() * 100
    st.metric("⚠️ Risiko Terlambat", f"{late_pct:.1f}%")
with col3:
    profit = dt['Order Item Profit Ratio'].sum()
    st.metric("💰 Total Profit Ratio", f"{profit:.2f}")

st.markdown("---")

# Distribusi Kategori
st.subheader("Distribusi Kategori")
categorical = ['Shipping Mode', 'Customer Segment', 'Order Region', 'Late_delivery_risk']
fig, axs = plt.subplots(2, 2, figsize=(14, 8))
for i, col in enumerate(categorical):
    ax = axs[i//2, i%2]
    sns.countplot(data=dt, x=col, ax=ax, palette="Set2",
                  order=dt[col].value_counts().index)
    ax.set_title(f"{col}")
    ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Tren Order per Bulan
st.subheader("📈 Volume Order per Bulan")
dt['Month'] = dt['order date (DateOrders)'].dt.to_period("M")
monthly_orders = dt.groupby('Month').size()
fig2, ax2 = plt.subplots(figsize=(12, 5))
monthly_orders.plot(kind='line', marker='o', ax=ax2, color='teal')
ax2.set_title("Jumlah Order per Bulan")
ax2.set_ylabel("Jumlah")
ax2.set_xlabel("Bulan")
plt.xticks(rotation=45)
st.pyplot(fig2)