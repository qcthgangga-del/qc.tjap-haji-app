import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="AI Quality Control - PT Tjap Haji Grup",
    page_icon="🍲",
    layout="wide"
)

# Konfigurasi Gemini API menggunakan API Key dari AI Studio / Secrets Streamlit
api_key = st.secrets.get("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)

st.title("🛡️ AI Quality Control Daily Check & Summary")
st.markdown("**PT Tjap Haji Grup (Warung Bakso Tjap Haji & Rumah Makan Tjap Ajam)**")

# Sidebar untuk Pilihan Restoran & Menu
st.sidebar.header("Navigasi & Restoran")
resto_pilihan = st.sidebar.selectbox(
    "Pilih Restoran Aktif",
    ["Warung Bakso Tjap Haji", "Rumah Makan Tjap Ajam"]
)

menu_pilihan = st.sidebar.radio(
    "Pilih Menu Aplikasi",
    ["Dashboard & Ringkasan", "Input Daily QC Check", "Non-Conformity Report (NCR)", "AI Daily Summary"]
)

if menu_pilihan == "Dashboard & Ringkasan":
    st.subheader(f"📊 Dashboard Mutu: {resto_pilihan}")
    st.info("Sistem pemantauan suhu, bahan baku, dan kepatuhan HACCP operasional harian aktif.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Inspeksi Bulan Ini", "24 Sesi", "+4 sesi")
    col2.metric("Pass Rate Mutu", "94.5%", "Standar >90%")
    col3.metric("Open NCR Aktif", "2 Kasus", "Perlu Tindakan")

elif menu_pilihan == "Input Daily QC Check":
    st.subheader(f"📝 Formulir QC Harian - {resto_pilihan}")
    
    with st.form("form_qc"):
        tanggal = st.date_input("Tanggal Inspeksi")
        outlet = st.selectbox("Pilih Cabang / Outlet", ["Cabang Dago Bandung", "Cabang Riau Bandung", "Cabang Jakarta"])
        shift = st.selectbox("Shift Kerja", ["Opening Shift", "Middle Shift", "Closing Shift"])
        
        st.markdown("---")
        st.markdown("### A. Pemeriksaan Bahan Baku & Suhu (CCP)")
        suhu_chilled = st.number_input("Suhu Aktual Bahan Baku Chilled (°C)", value=2.5, step=0.1)
        
        catatan = st.text_area("Catatan Kondisi Umum & Kebersihan Saji")
        
        submitted = st.form_submit_button("Kirim Laporan QC")
        if submitted:
            st.success(f"Laporan QC untuk {resto_pilihan} di {outlet} berhasil disimpan secara mandiri!")

elif menu_pilihan == "Non-Conformity Report (NCR)":
    st.subheader("⚠️ Manajemen Temuan Ketidaksesuaian (NCR)")
    st.write("Catat dan pantau penyimpangan mutu beserta tindakan korektif (CAPA) langsung di sini.")

elif menu_pilihan == "AI Daily Summary":
    st.subheader("✨ AI Daily Summary (Gemini API)")
    st.write("Hasilkan ringkasan manajemen harian otomatis menggunakan model Gemini Flash.")
    
    if st.button("Generate Ringkasan Eksekutif AI"):
        with st.spinner("AI sedang menganalisis data laporan..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Buatkan ringkasan eksekutif QC harian untuk operasional {resto_pilihan} di bawah PT Tjap Haji Grup.")
                st.success("Ringkasan Berhasil Dibuat!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Gagal memanggil AI (Pastikan API Key sudah terpasang): {e}")