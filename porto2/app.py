import streamlit as st

# Konfigurasi halaman wajib di paling atas
st.set_page_config(
    page_title="Operational Command Center | Data Analytics",
    page_icon="⚙️",
    layout="wide"
)
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
