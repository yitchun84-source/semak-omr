import streamlit as st
import cv2
import numpy as np

st.set_page_config(layout="wide")
st.title("🖨️ Pengimbas OMR: Instrumen Aptitud Am Tahun 4")
st.subheader("Borang Jawapan Objektif (80 Soalan)")

# --- 1. PENYEDIAAN SKEMA JAWAPAN (80 SOALAN) ---
st.sidebar.header("🔑 Tetapkan Skema Jawapan")
skema_jawapan = {}

# Buat tab di sidebar supaya kemas mengikut sub-kategori
tab_bm, tab_bi, tab_mat = st.sidebar.tabs(["Bahasa Melayu", "Bahasa Inggeris", "Matematik"])

with tab_bm:
    st.write("**BM (Soalan 1 - 30)**")
    for i in range(1, 31):
        skema_jawapan[i] = st.selectbox(f"No {i}", ["A", "B", "C", "D"], key=f"bm_{i}")

with tab_bi:
    st.write("**BI (Soalan 31 - 55)**")
    for i in range(31, 56):
        skema_jawapan[i] = st.selectbox(f"No {i}", ["A", "B", "C", "D"], key=f"bi_{i}")

with tab_mat:
    st.write("**Matematik (Soalan 56 - 80)**")
    for i in range(56, 81):
        skema_jawapan[i] = st.selectbox(f"No {i}", ["A", "B", "C", "D"], key=f"mat_{i}")

# --- 2. PROSES PENGIMBASAN ---
uploaded_file = st.file_uploader("Muat naik fail gambar Borang Jawapan OMR", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    output = image.copy()
    
    # Tukar ke format hitam putih & cari bulatan
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bulatan_all = []
    
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        aspek_nisbah = w / float(h)
        if w >= 15 and h >= 15 and 0.85 <= aspek_nisbah <= 1.15: # Melonggarkan sedikit julat saiz
            bulatan_all.append(c)
            cv2.drawContours(output, [c], -1, (0, 255, 255), 2)
            
    # Paparkan maklumat analisis di skrin
    st.write(f"📊 **Analisis Imbasan:** Sistem mengesan **{len(bulatan_all)}** bulatan daripada sepatutnya **320** bulatan.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(output, channels="BGR", caption="Hasil Pengesanan Bulatan (Kuning)", use_container_width=True)
        
    with col2:
        if len(bulatan_all) == 320:
            st.success("✅ Semua bulatan dikesan dengan sempurna! Sedia untuk pengiraan markah.")
            # Di sini kita akan letakkan kod menyusun (sorting) mengikut lajur pada fasa akhir nanti.
        else:
            st.warning("⚠️ Jumlah bulatan tidak tepat 320. Pastikan borang diimbas secara rata, tiada kawasan tulisan nama yang mengganggu, dan kualiti gambar adalah tinggi.")
