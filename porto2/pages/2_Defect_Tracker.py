import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

st.set_page_config(page_title="Defect & Pareto Tracker", page_icon="🏭", layout="wide")

st.title("🏭 Manufacturing Defect & Cost Tracker")
st.markdown("Pemantauan *Quality Control* (QC) preskriptif dan audit kerugian berbasis **Hukum Pareto (80/20)**.")
st.markdown("---")

@st.cache_data
def load_defect_data():
    df = pd.read_csv('datasets/defects_data.csv')
    df['defect_date'] = pd.to_datetime(df['defect_date'])
    return df

try:
    df = load_defect_data()
except FileNotFoundError:
    st.error("Gagal memuat data. Pastikan file 'defects_data.csv' berada di dalam folder 'datasets/'.")
    st.stop()

# --- SIDEBAR PARAMETERS ---
st.sidebar.header("⚙️ Filter Lantai Produksi")
lokasi_mesin = st.sidebar.multiselect("Lokasi / Mesin:", options=df['defect_location'].unique(), default=df['defect_location'].unique())
tingkat_keparahan = st.sidebar.multiselect("Tingkat Keparahan (Severity):", options=df['severity'].unique(), default=df['severity'].unique())

df_filtered = df[(df['defect_location'].isin(lokasi_mesin)) & (df['severity'].isin(tingkat_keparahan))]

# --- 1. KPI EKSEKUTIF ---
total_cacat = len(df_filtered)
total_kerugian = df_filtered['repair_cost'].sum()
avg_kerugian = df_filtered['repair_cost'].mean() if total_cacat > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Insiden Cacat", f"{total_cacat} Kasus", "Membutuhkan Tindakan QC", delta_color="inverse")
col2.metric("Total Biaya Perbaikan (Loss)", f"${total_kerugian:,.2f}", "- Kebocoran Anggaran", delta_color="inverse")
col3.metric("Rata-rata Biaya per Insiden", f"${avg_kerugian:,.2f}")

st.divider()

# --- 2. AUTOMATED PRESCRIPTIVE INSIGHT (THE "WOW" FACTOR) ---
st.subheader("🧠 Algoritma Rekomendasi Sistem")
if not df_filtered.empty:
    cost_by_location = df_filtered.groupby('defect_location')['repair_cost'].sum().reset_index().sort_values(by='repair_cost', ascending=False)
    top_bleeder = cost_by_location.iloc[0]
    persentase_kebocoran = (top_bleeder['repair_cost'] / total_kerugian) * 100
    
    st.error(f"🚨 **TINDAKAN KRITIS DIPERLUKAN:** Area **{top_bleeder['defect_location']}** adalah sumber kebocoran finansial terbesar, membakar **${top_bleeder['repair_cost']:,.2f}** ({persentase_kebocoran:.1f}% dari total kerugian yang difilter). Segera jadwalkan kalibrasi mesin atau inspeksi QC di area ini pada *shift* berikutnya.")
else:
    st.success("Sistem aman. Tidak ada anomali terdeteksi.")

st.divider()

# --- 3. PARETO CHART ANALYSIS (ADVANCED ANALYTICS) ---
st.subheader("📊 Analisis Pareto (Hukum 80/20 Kerugian Manufaktur)")
st.markdown("Mengidentifikasi sedikit penyebab yang menghasilkan sebagian besar kerugian.")

if not df_filtered.empty:
    # Kalkulasi Pareto (Cumulative Percentage)
    pareto_data = cost_by_location.copy()
    pareto_data['cumulative_cost'] = pareto_data['repair_cost'].cumsum()
    pareto_data['cumulative_percent'] = (pareto_data['cumulative_cost'] / total_kerugian) * 100

    # Membuat Grafik Kombinasi (Bar + Line) dengan Plotly Graph Objects
    fig_pareto = go.Figure()
    
    # Tambahkan Bar Chart untuk Biaya
    fig_pareto.add_trace(go.Bar(
        x=pareto_data['defect_location'], y=pareto_data['repair_cost'],
        name="Total Kerugian ($)", marker_color='indianred'
    ))
    
    # Tambahkan Line Chart untuk Persentase Kumulatif
    fig_pareto.add_trace(go.Scatter(
        x=pareto_data['defect_location'], y=pareto_data['cumulative_percent'],
        name="Persentase Kumulatif (%)", yaxis="y2", mode='lines+markers',
        line=dict(color='navy', width=3)
    ))
    
    # Konfigurasi 2 Axis (Kiri dan Kanan)
    fig_pareto.update_layout(
        title="Distribusi Kerugian Finansial per Lokasi (Pareto Curve)",
        yaxis=dict(title="Total Kerugian ($)"),
        yaxis2=dict(title="Persentase Kumulatif (%)", overlaying="y", side="right", range=[0, 110]),
        legend=dict(x=0.01, y=0.99)
    )
    st.plotly_chart(fig_pareto, use_container_width=True)

st.divider()

# --- 4. TABEL AUDIT & EKSPOR ---
st.subheader("🚨 Log Inspeksi Kritis & Rencana Perbaikan")

cols_to_show = ['defect_date', 'defect_location', 'defect_type', 'severity', 'repair_cost', 'inspection_method']
df_export = df_filtered[cols_to_show].sort_values(by='repair_cost', ascending=False)
st.dataframe(df_export, use_container_width=True)

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    df_export.to_excel(writer, index=False, sheet_name='Audit_Cacat_Produksi')

st.download_button(
    label="📥 Ekspor Data QC ke Excel",
    data=buffer.getvalue(),
    file_name="Laporan_Kerugian_Produksi.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    type="primary"
)