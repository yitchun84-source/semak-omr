import streamlit as st
import cv2
import numpy as np

st.title("🖨️ Sistem Pengimbas OMR Komputer")
st.write("Aplikasi anda kini sudah aktif di awan!")

uploaded_file = st.file_uploader("Muat naik gambar kertas OMR", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    st.image(image, channels="BGR", caption="Gambar Berjaya Dimuat Naik")
    st.success("Sistem sedia memproses!")
