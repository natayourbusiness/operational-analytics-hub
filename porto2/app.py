import streamlit as st
import os
# Konfigurasi halaman wajib di paling atas
st.set_page_config(
    page_title="Operational Command Center | Data Analytics",
    page_icon="⚙️",
    layout="wide"
)

# Header Eksekutif
st.title("⚙️ Supply Chain & Retail Analytics Hub")
st.markdown("---")
st.error("🚨 MODE DEBUG AKTIF: Membedah Isi Server")
st.write("**1. Posisi Direktori Saat Ini (Working Directory):**", os.getcwd())

st.write("**2. Apa saja file dan folder yang ada di lokasi ini?**")
st.write(os.listdir())

if os.path.isdir('datasets'):
    st.write("**3. Folder 'datasets' DITEMUKAN. Ini isinya:**")
    st.write(os.listdir('datasets'))
else:
    st.error("❌ FOLDER 'datasets' TIDAK DITEMUKAN oleh mesin di lokasi ini!")

st.stop()
# Pesan Pengantar
st.markdown("""
### **Mengubah Data Mentah Menjadi Keputusan Operasional**

Sistem otomasi dan analitik ini dirancang khusus untuk mengeliminasi *human error* pada pemrosesan data bervolume tinggi di sektor manufaktur, logistik, dan ritel. 

**Pilih modul operasional di sidebar kiri untuk memulai simulasi:**
1. **Sales & Revenue Audit:** Deteksi kebocoran arus kas dari pesanan bermasalah.
2. **Manufacturing Defect Tracker:** Analisis kerugian finansial di lantai produksi akibat cacat barang.
3. **Inventory Health & Expiry:** Audit stok gudang dan pelacakan barang mendekati kedaluwarsa.

---
""")

# Informasi Kontak & Profesionalisme
st.info("""
**Dikembangkan oleh:** Rio | B.Eng in Informatics Engineering  
*Fokus pada efisiensi prosedural, validasi 'zero-error', dan otomasi data.*
""")

st.caption("Peringatan: Seluruh data yang digunakan dalam Command Center ini adalah data untuk keperluan demonstrasi audit sistem operasional.")
