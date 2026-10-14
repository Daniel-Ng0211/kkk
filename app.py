import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Cau hinh trang web
st.set_page_config(
    page_title="Quan ly diem sinh vien",
    page_icon="📚",
    layout="wide"
)

st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 1. Tao DataFrame
data = {
    "Ho_ten": [
       'Nguyễn Thành Đạt',
       'Trương Quốc Đạt',
       'Nguyễn Tuấn Khang',
       'Bùi Anh Tuấn',
       'Lê Nguyễn Anh Kiệt',
       'Đỗ Xuân Hoài',
       'Võ Huy Khánh',
       'Lê Công Trường Hận',
       'Võ Thị Công Lý',
       'Phạm Mai Kiều Vi'
    ],
    "Chuyen_can": [9, 8, 7, 4, 8, 9, 5, 8, 7, 10],
    "Giua_ky":    [8, 7, 6, 7, 9, 8, 4, 7, 6, 9],
    "Cuoi_ky":    [9, 8, 7, 5, 8, 9, 5, 8, 6, 10]
}

df = pd.DataFrame(data)

# 2. Tinh diem tong ket
df["Tong_ket"] = (
    df["Chuyen_can"] * 0.2
    + df["Giua_ky"] * 0.3
    + df["Cuoi_ky"] * 0.5
)

# 3. Xep loai sinh vien
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 4. Hien thi bang diem
st.subheader("1. Bảng điểm sinh viên")

bang_diem = df[
    [
        "Ho_ten", "Chuyen_can",
        "Giua_ky", "Cuoi_ky", "Tong_ket", "Xep_loai"
    ]
].rename(columns={
    "Ho_ten": "Họ và tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})

st.dataframe(
    bang_diem.round(2),
    use_container_width=True,
    hide_index=True
)

# 5. Thong ke
st.subheader("2. Thống kê kết quả học tập")

diem_tb = df["Tong_ket"].mean()
idx_max = df["Tong_ket"].idxmax()
idx_min = df["Tong_ket"].idxmin()
so_dat = (df["Tong_ket"] >= 5).sum()

col1, col2, col3 = st.columns(3)

col1.metric("Điểm trung bình lớp", f"{diem_tb:.2f}")
tong_sv = len(df)

col2.metric("Số sinh viên đạt", f"{so_dat}/{tong_sv}")
col3.metric("Số sinh viên chưa đạt", f"{tong_sv - so_dat}/{tong_sv}")
col4, col5 = st.columns(2)

with col4:
    st.write("**Sinh viên có điểm cao nhất**")
    st.success(
        f"{df.loc[idx_max, 'Ho_ten']} - "
        f"{df.loc[idx_max, 'Tong_ket']:.2f} điểm"
    )

with col5:
    st.write("**Sinh viên có điểm thấp nhất**")
    st.warning(
        f"{df.loc[idx_min, 'Ho_ten']} - "
        f"{df.loc[idx_min, 'Tong_ket']:.2f} điểm"
    )

# 6. Selectbox chon sinh vien
st.subheader("3. Tra cứu điểm sinh viên")

ten_sv = st.selectbox(
    "Chọn sinh viên:",
    df["Ho_ten"].tolist()
)

sv = df[df["Ho_ten"] == ten_sv].iloc[0]

st.write(f"**Họ và tên:** {sv['Ho_ten']}")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Chuyên cần", f"{sv['Chuyen_can']:.1f}")
c2.metric("Giữa kỳ", f"{sv['Giua_ky']:.1f}")
c3.metric("Cuối kỳ", f"{sv['Cuoi_ky']:.1f}")
c4.metric("Tổng kết", f"{sv['Tong_ket']:.2f}")
c5.metric("Xếp loại", sv["Xep_loai"])

# 7. Ve bieu do Matplotlib
st.subheader("4. Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.barh(
    df["Ho_ten"],
    df["Tong_ket"],
    color="skyblue",
    edgecolor="black"
)

ax.set_title("ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN")
ax.set_ylabel("Họ và tên sinh viên")
ax.set_xlabel("Điểm tổng kết")
ax.set_xlim(0, 10)

ax.bar_label(bars, fmt="%.2f", padding=3)
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="x", linestyle="--", alpha=0.4)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# 8. Thong tin nguoi tao
st.divider()
st.caption("Người tạo ứng dụng: Nguyễn Thành Đạt | MSSV: 060208012809")