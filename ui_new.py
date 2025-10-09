import streamlit as st
import pandas as pd
import os
from pathlib import Path


st.set_page_config(
    page_title="Danh mục xếp hạng",
    page_icon="Mega.jpg",  
    layout="wide"
)



# --- Load dữ liệu ---
file_path = os.path.join("result", "summary.xlsx")

@st.cache_data
def load_data():
    return pd.read_excel(file_path)

df = load_data()


# --- Logo + tiêu đề căn giữa ---
logo_path = Path("Mega2.png") 
if logo_path.exists():
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col3:   # căn giữa ảnh
        st.image(str(logo_path), width=720)

st.markdown(
    "<h1 style='text-align: center;'>DANH MỤC XẾP HẠNG</h1>",
    unsafe_allow_html=True
)



# --- Thanh tìm kiếm nhiều mã ---
search_input = st.text_input("Nhập mã cổ phiếu (ví dụ: ACB, HDB, CTG...):")
tickers = [x.strip().upper() for x in search_input.replace(" ", ",").split(",") if x.strip()]


# --- Bộ lọc theo Model ---
model_filter = st.selectbox("Chọn mô hình:", ["Tất cả", "Ngân hàng", "Phi tài chính", "Chứng khoán"])

# --- Bộ lọc theo Grade ---
grade_filter = st.multiselect("Chọn điểm:", options=sorted(df["Điểm"].unique()))

# --- Slider chọn số lượng hiển thị ---
top_n = st.slider("Số lượng tối đa muốn hiển thị:", 30, 300, 50)

# Áp dụng filter
filtered = df.copy()
if tickers:
    filtered = filtered[filtered["Mã"].isin(tickers)]
    
if model_filter != "Tất cả":
    filtered = filtered[filtered["Mô hình"] == model_filter]

if grade_filter:
    filtered = filtered[filtered["Điểm"].isin(grade_filter)]

# --- Hiển thị kết quả ---
st.write(f"Có {len(filtered)} kết quả sau khi lọc")
st.dataframe(filtered.head(top_n), use_container_width=True)

from io import BytesIO

# --- Xuất Excel ---
if not filtered.empty:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        filtered.to_excel(writer, index=False, sheet_name="KQ")

    st.download_button(
        label="Tải kết quả lọc về Excel",
        data=buffer.getvalue(),
        file_name="ket_qua_loc.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
