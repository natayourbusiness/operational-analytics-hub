import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Sales Analytics", page_icon="📈", layout="wide")

st.title("📈 Advanced Sales & Revenue Analytics")
st.markdown("Audit performa penjualan komprehensif menggunakan analisis Pareto dan deteksi anomali transaksi.")
st.markdown("---")

@st.cache_data
def load_sales_data():
    df = pd.read_csv('datasets/sales_data_sample.csv', encoding='latin1')
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
    return df

try:
    df = load_sales_data()
except FileNotFoundError:
    st.error("Gagal memuat data. Periksa folder datasets.")
    st.stop()

# --- SIDEBAR PARAMETERS ---
st.sidebar.header("⚙️ Parameter Analitik")
tahun_pilihan = st.sidebar.multiselect("Pilih Tahun:", options=df['YEAR_ID'].unique(), default=df['YEAR_ID'].unique() )
lini_produk = st.sidebar.multiselect("Lini Produk:", options=df['PRODUCTLINE'].unique(), default=df['PRODUCTLINE'].unique())
df_filtered = df[(df['YEAR_ID'].isin(tahun_pilihan)) & (df['PRODUCTLINE'].isin(lini_produk))]


# --- 1. CORE ANALYTICS METRICS ---
total_revenue = df_filtered['SALES'].sum()
total_orders = df_filtered['ORDERNUMBER'].nunique()
aov = total_revenue / total_orders if total_orders > 0 else 0

problem_status = ['Cancelled', 'On Hold', 'Disputed']
df_problem = df_filtered[df_filtered['STATUS'].isin(problem_status)]
money_leaked = df_problem['SALES'].sum()
total_problem_orders = df_problem['ORDERNUMBER'].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Pendapatan (Gross)", f"${total_revenue:,.0f}")
col2.metric("Total Transaksi", f"{total_orders}")
col3.metric("Average Order Value (AOV)", f"${aov:,.0f}", "Nilai rata-rata per transaksi")
col4.metric("Potensi Kebocoran (Kas Tertahan)", f"${money_leaked:,.0f}", "- Membutuhkan Audit", delta_color="inverse")

st.divider()

# --- 2. PARETO & PRODUCT PERFORMANCE (PLOTLY) ---
st.subheader("📊 Analisis Distribusi Lini Produk (Pareto & Proporsi)")

col_bar, col_pie = st.columns(2)

with col_bar:
    # Bar Chart Interaktif
    sales_by_product = df_filtered.groupby('PRODUCTLINE')['SALES'].sum().reset_index().sort_values(by='SALES', ascending=False)
    fig_bar = px.bar(sales_by_product, x='PRODUCTLINE', y='SALES', 
                text_auto=True, 
                title="Pendapatan Berdasarkan Lini Produk",
                color='SALES', color_continuous_scale='Blues')
    fig_bar.update_layout(xaxis_title="Lini Produk", yaxis_title="Total Pendapatan ($)")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_pie:
    # Donut Chart untuk Proporsi
    fig_pie = px.pie(sales_by_product, values='SALES', names='PRODUCTLINE', hole=0.4,
                     title="Proporsi Pangsa Pasar (Market Share)")
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# --- 3. CUSTOMER VALUE SCATTER (KORELASI ANALISIS) ---
st.subheader("🎯 Pemetaan Nilai Pelanggan (Customer Value Correlation)")
st.markdown("Menganalisis korelasi antara besaran kuantitas pesanan dengan total nilai transaksi per pelanggan untuk mendeteksi *Key Accounts*.")

# Scatter plot menggunakan plotly
customer_data = df_filtered.groupby('CUSTOMERNAME').agg({'SALES': 'sum', 'QUANTITYORDERED': 'sum', 'STATUS': 'first'}).reset_index()
fig_scatter = px.scatter(customer_data, x='QUANTITYORDERED', y='SALES', 
                         color='SALES', size='SALES', hover_name='CUSTOMERNAME',
                         title="Kuantitas Dipesan vs Total Nilai Transaksi",
                         color_continuous_scale='Teal')
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# --- 4. EXPORT ENGINE (ZERO-ERROR AUDIT) ---
st.subheader("🚨 Ekstraksi Data Anomali (Ekspor Excel)")

if not df_problem.empty:
    st.error(f"Ditemukan {len(df_problem)} item pesanan dengan status bermasalah.")
    cols_to_show = ['ORDERNUMBER', 'ORDERDATE', 'STATUS', 'CUSTOMERNAME', 'PRODUCTLINE', 'SALES']
    df_export = df_problem[cols_to_show].sort_values(by='SALES', ascending=False)
    st.dataframe(df_export, use_container_width=True)
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_export.to_excel(writer, index=False, sheet_name='Audit_Anomali')
    
    st.download_button(
        label="📥 Ekspor Laporan Anomali ke Excel",
        data=buffer.getvalue(),
        file_name="Laporan_Anomali_Penjualan.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )
else:
    st.success("Tidak ada anomali terdeteksi pada rentang waktu terpilih.")
