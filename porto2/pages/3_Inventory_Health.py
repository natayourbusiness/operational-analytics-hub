import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from datetime import datetime

st.set_page_config(page_title="Inventory Health Audit", page_icon="📦", layout="wide")

st.title("📦 Inventory Health & Expiry Audit")
st.markdown("Audit otomatis untuk mencegah kerugian barang kedaluwarsa (*Dead Stock*) dan memantau peringatan batas ulang pemesanan (*Reorder Level*).")
st.markdown("---")

# 1. LOAD DATA & THE ULTIMATE DATA CLEANER
@st.cache_data
def load_inventory_data():
    # utf-8-sig menghancurkan karakter hantu (BOM) di awal file
    df = pd.read_csv('datasets/grocery_inventory.csv', encoding='utf-8-sig')
    
    # MESIN PEMBERSIH KOLOM: Hilangkan spasi ujung, ubah jadi huruf kecil, ganti spasi jadi underscore
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Pemetaan paksa nama kolom kotor menjadi nama standar yang kita butuhkan
    col_mapping = {
        'catagory': 'Category',
        'category': 'Category',
        'product_name': 'Product_Name',
        'expiration_date': 'Expiration_Date',
        'stock_quantity': 'Stock_Quantity',
        'reorder_level': 'Reorder_Level',
        'unit_price': 'Unit_Price',
        'supplier_name': 'Supplier_Name',
        'reorder_quantity': 'Reorder_Quantity'
    }
    df.rename(columns=col_mapping, inplace=True)
    
    # Validasi jika kolom masih ada yang hilang
    required_cols = ['Product_Name', 'Category', 'Expiration_Date', 'Stock_Quantity', 'Reorder_Level', 'Unit_Price']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.error(f"🚨 FATAL ERROR: Dataset Anda tidak memiliki kolom berikut: {missing_cols}")
        st.warning(f"Berikut adalah daftar nama kolom asli yang terbaca oleh sistem: {list(df.columns)}")
        st.stop() # Hentikan aplikasi agar tidak error panjang

    # Proses kalkulasi bisnis
    df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'], errors='coerce')
    kolom_angka = ['Stock_Quantity', 'Unit_Price', 'Reorder_Level', 'Reorder_Quantity']
    for col in kolom_angka:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'[\$,\s]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df['Total_Value'] = df['Stock_Quantity'] * df['Unit_Price']
    return df

df = load_inventory_data()

# 2. SIDEBAR PARAMETERS & TIME MACHINE
st.sidebar.header("⚙️ Parameter Audit Gudang")

default_today = df['Expiration_Date'].min() if pd.notnull(df['Expiration_Date'].min()) else datetime.today()
tanggal_audit = st.sidebar.date_input("Tanggal Audit Simulasi (Hari Ini):", value=default_today)

# Menggunakan 'Category' karena sudah diseragamkan oleh mesin pembersih di atas
kategori_pilihan = st.sidebar.multiselect("Kategori Produk:", options=df['Category'].unique(), default=df['Category'].unique())
df_filtered = df[df['Category'].isin(kategori_pilihan)].copy()

tanggal_audit = pd.to_datetime(tanggal_audit)
df_filtered['Days_to_Expiry'] = (df_filtered['Expiration_Date'] - tanggal_audit).dt.days

# 3. KATEGORISASI KESEHATAN STOK
df_expired = df_filtered[df_filtered['Days_to_Expiry'] < 0]
df_critical = df_filtered[(df_filtered['Days_to_Expiry'] >= 0) & (df_filtered['Days_to_Expiry'] <= 30)]
df_reorder = df_filtered[df_filtered['Stock_Quantity'] <= df_filtered['Reorder_Level']]

# --- KPI EKSEKUTIF ---
total_inventory_value = df_filtered['Total_Value'].sum()
loss_expired = df_expired['Total_Value'].sum()
risk_critical = df_critical['Total_Value'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Valuasi Gudang", f"${total_inventory_value:,.0f}")
col2.metric("Kerugian Kedaluwarsa (Loss)", f"${loss_expired:,.0f}", f"{len(df_expired)} SKU", delta_color="inverse")
col3.metric("Risiko Kritis (< 30 Hari)", f"${risk_critical:,.0f}", f"{len(df_critical)} SKU", delta_color="inverse")
col4.metric("Peringatan Reorder (Stok Tipis)", f"{len(df_reorder)} SKU", "Segera PO ke Supplier", delta_color="inverse")

st.divider()

# --- AUTOMATED PRESCRIPTIVE INSIGHT ---
st.subheader("🧠 Rekomendasi Tindakan Cepat (Purchasing & Warehouse)")

if not df_critical.empty:
    st.error(f"🚨 **TINDAKAN PROMO DIBUTUHKAN:** Terdapat {len(df_critical)} produk dengan nilai total **${risk_critical:,.0f}** yang akan kedaluwarsa dalam 30 hari ke depan.")
else:
    st.success("Tidak ada produk dengan risiko kedaluwarsa tinggi dalam 30 hari ke depan.")

if not df_reorder.empty:
    st.warning(f"⚠️ **PERINGATAN PURCHASING:** {len(df_reorder)} produk telah menyentuh atau berada di bawah batas minimum (*Reorder Level*).")

st.divider()

# --- VISUALISASI ANALITIK KESEHATAN GUDANG ---
col_scatter, col_bar = st.columns(2)

with col_scatter:
    st.markdown("**Pemetaan Kritis: Stok Aktual vs Batas Minimum**")
    fig_scatter = px.scatter(df_filtered, x='Reorder_Level', y='Stock_Quantity', 
                             color='Category', hover_name='Product_Name',
                             labels={'Stock_Quantity': 'Stok Tersedia', 'Reorder_Level': 'Batas Pesan Ulang'})
    max_val = max(df_filtered['Reorder_Level'].max(), df_filtered['Stock_Quantity'].max())
    fig_scatter.add_trace(go.Scatter(x=[0, max_val], y=[0, max_val], mode='lines', name='Batas Bahaya', line=dict(color='red', dash='dash')))
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_bar:
    st.markdown("**Distribusi Risiko Finansial (Barang Kritis < 30 Hari)**")
    if not df_critical.empty:
        risk_by_cat = df_critical.groupby('Category')['Total_Value'].sum().reset_index()
        fig_bar = px.bar(risk_by_cat, x='Category', y='Total_Value', text_auto= True,
                         color='Total_Value', color_continuous_scale='Oranges')
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Tidak ada data kritis untuk divisualisasikan.")

st.divider()

# --- TABEL EKSPOR (THE GOLDEN BUTTONS) ---
st.subheader("🚨 Ekstraksi Data Audit")

tab1, tab2 = st.tabs(["📝 Daftar Produk Kritis (Expiry Audit)", "🛒 Daftar Permintaan Pembelian (Reorder List)"])

with tab1:
    # Menggunakan daftar kolom dinamis untuk mencegah error jika ada kolom yang benar-benar tidak eksis
    cols_tab1 = [c for c in ['Product_Name', 'Category', 'Expiration_Date', 'Days_to_Expiry', 'Stock_Quantity', 'Total_Value'] if c in df_critical.columns]
    st.dataframe(df_critical[cols_tab1].sort_values(by='Days_to_Expiry'), use_container_width=True)
    
    buffer_expiry = io.BytesIO()
    with pd.ExcelWriter(buffer_expiry, engine='openpyxl') as writer:
        df_critical.to_excel(writer, index=False, sheet_name='Audit_Kedaluwarsa')
    st.download_button("📥 Ekspor Laporan Kedaluwarsa ke Excel", data=buffer_expiry.getvalue(), file_name="Laporan_Kedaluwarsa.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

with tab2:
    cols_tab2 = [c for c in ['Product_Name', 'Supplier_Name', 'Stock_Quantity', 'Reorder_Level', 'Reorder_Quantity', 'Unit_Price'] if c in df_reorder.columns]
    st.dataframe(df_reorder[cols_tab2].sort_values(by='Stock_Quantity'), use_container_width=True)
    
    buffer_reorder = io.BytesIO()
    with pd.ExcelWriter(buffer_reorder, engine='openpyxl') as writer:
        df_reorder.to_excel(writer, index=False, sheet_name='Daftar_PO')
    st.download_button("📥 Ekspor Laporan Reorder (PO) ke Excel", data=buffer_reorder.getvalue(), file_name="Laporan_Reorder_Supplier.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")