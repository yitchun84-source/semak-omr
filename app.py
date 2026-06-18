import streamlit as st
import cv2
import numpy as np

st.set_page_config(layout="wide")
st.title("🖨️ Sistem Pengimbas OMR Komputer (Versi Imbasan Asas)")

# 1. SET SKEMA JAWAPAN (Sisi Kiri)
st.sidebar.header("🔑 Set Skema Jawapan")
skema = []
for i in range(1, 6): # Contoh untuk 5 soalan dahulu
    jawapan = st.sidebar.selectbox(f"Soalan {i}", ["A", "B", "C", "D"], key=f"skema_{i}")
    pemetaan = {"A": 0, "B": 1, "C": 2, "D": 3}
    skema.append(pemetaan[jawapan])

# 2. RUANG MUAT NAIK GAMBAR
uploaded_file = st.file_uploader("Muat naik gambar kertas OMR (Format: JPG, PNG)", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Tukar fail kepada format imej OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    output_image = image.copy()
    
    # --- PROSES COMPUTER VISION ---
    # 1. Tukar ke Hitam-Putih (Grayscale)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 2. Kurangkan kabur (Blur)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # 3. Tukar ke Binary (Hitam Pekat & Putih Pekat)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    # 4. Cari bentuk kontur (bulatan)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bulatan_jawapan = []
    
    # Tapis objek yang betul-betul berbentuk bulat sahaja
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        aspek_nisbah = w / float(h)
        # Sifat bulatan: lebar dan tinggi hampir sama, saiz sederhana
        if w >= 20 and h >= 20 and 0.9 <= aspek_nisbah <= 1.1:
            bulatan_jawapan.append(c)
            # Lukis garisan kuning pada setiap bulatan yang ditemui komputer
            cv2.drawContours(output_image, [c], -1, (0, 255, 255), 2)
            
    # --- PAPARAN KEPUTUSAN ---
    st.write(f"🔍 **Analisis Komputer:** Sistem mengesan **{len(bulatan_jawapan)}** bulatan pada kertas ini.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🖼️ Hasil Imbasan")
        st.image(output_image, channels="BGR", caption="Bulatan kuning bermaksud dikesan oleh komputer", use_container_width=True)
        
    with col2:
        st.subheader("📝 Nota Panduan")
        st.info("Untuk membolehkan sistem mengira markah dengan tepat, jumlah bulatan yang dikesan mestilah genap mengikut bilangan soalan (Contoh: 5 soalan x 4 pilihan = 20 bulatan).")
        
        if len(bulatan_jawapan) != 20:
            st.warning("⚠️ Jumlah bulatan belum mencukupi 20. Sila pastikan gambar kertas OMR anda diambil secara tegak, terang, dan tiada bayang gelap.")
