import streamlit as st

# Konfigurasi halaman wajib di paling atas
st.set_page_config(
    page_title="Portofolio Donny",
    page_icon="⚙️",
    layout="wide"
)
# Pesan Pengantar
st.markdown("""
### **Portofolio Donny Pranata**

**Data yang berantakan adalah biaya operasional tersembunyi. Saya di sini untuk mengubahnya menjadi strategi.**

Selamat datang di *Automated Operations Command Center.*

Sebagai seorang "Data Analyst and Operations Professional" dengan fondasi kuat dalam "HR analytics, inventory management, and ERP systems", saya tidak sekadar membuat dasbor yang terlihat bagus. Saya membangun arsitektur analitik yang memecahkan masalah nyata.  

Aplikasi ini adalah bukti langsung bagaimana "raw operational datasets" dapat diekstraksi dan ditransformasi menjadi "strategic insights" yang dapat ditindaklanjuti oleh manajemen untuk menghentikan inefisiensi.  

🛠️ **Core Architecture:**
Dibangun menggunakan *"Python, Streamlit, and SQL"* dengan implementasi pemodelan *"Relational Database Architecture"* dan algoritma *"K-Means clustering".*  

📊 **Modul Operasional (Proof of Concept):**

Jangan hanya membaca CV saya. Uji langsung sistem yang telah saya rancang dengan memilih modul di bawah ini:

📦 **Inventory Health & Expiry Audit**
    Sistem rantai pasok prediktif yang secara otomatis menghitung "days-to-expiry and reorder thresholds" untuk mencegah *"dead-stock financial loss".*  

🏭 **Manufacturing Defect & Cost Tracker**
    Alat "root-cause analysis" yang melacak anomali produksi, mengkuantifikasi *"financial leakage"*, dan meresepkan intervensi *"Quality Control (QC)"* secara presisi.  

💼 **Advanced Sales & Revenue Audit**
    Mesin audit dinamis yang mengintegrasikan *"Pareto (80/20) analysis"* untuk mengidentifikasi *"top-performing product lines"* dan memetakan nilai pelanggan.  

👈 **Buka navigasi di Sidebar Kiri untuk memulai simulasi sistem.**

---
""")

# Informasi Kontak & Profesionalisme
st.info("""
**Dikembangkan oleh:** Donny Pranata| Bachelor in Informatics Engineering  
*Fokus pada efisiensi prosedural, validasi 'zero-error', dan otomasi data.*
""")

st.caption("Peringatan: Seluruh data yang digunakan dalam Command Center ini adalah data untuk keperluan demonstrasi audit sistem operasional.")
