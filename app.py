import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# ==========================================
# 1. TẠO DATAFRAME
# ==========================================
data = {
    'Ho_ten': [
        'An',
        'Bình',
        'Chi',
        'Dũng',
        'Hà',
        'Lan',
        'Minh',
        'Nam',
        'Phúc',
        'Trang',
    ],
    'Chuyen_can': [8.5, 9.0, 7.0, 9.5, 8.0, 6.0, 9.0, 7.5, 8.0, 10.0],
    'Giua_ky': [7.5, 8.5, 6.5, 9.0, 7.0, 5.5, 8.5, 7.0, 7.5, 9.0],
    'Cuoi_ky': [8.0, 8.5, 6.0, 9.0, 7.5, 6.0, 8.5, 6.5, 7.5, 9.0],
}
df = pd.DataFrame(data)

# ==========================================
# 2. TÍNH ĐIỂM TỔNG KẾT VÀ XẾP LOẠI
# ==========================================
df['Tong_ket'] = (
    0.2 * df['Chuyen_can'] + 0.3 * df['Giua_ky'] + 0.5 * df['Cuoi_ky']
).round(2)

def xep_loai(diem):
  if diem >= 8.5:
    return 'Giỏi'
  elif diem >= 7.0:
    return 'Khá'
  elif diem >= 5.0:
    return 'Trung bình'
  else:
    return 'Yếu'
df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)
# ==========================================
# GIAO DIỆN STREAMLIT WEB APP
# ==========================================
# Tiêu đề Web App
st.title('QUẢN LÝ ĐIỂM SINH VIÊN')
# Hiển thị Bảng điểm
st.subheader('📋 Bảng điểm sinh viên')
st.dataframe(df, use_container_width=True)
# #3. THỐNG KÊ
st.subheader('📊 Thống kê')
dtb_lop = df['Tong_ket'].mean()
sv_cao_nhat = df.loc[df['Tong_ket'].idxmax()]
sv_thap_nhat = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()
col1, col2 = st.columns(2)
with col1:
  st.metric(label='ĐTB cả lớp', value=f'{dtb_lop:.2f}')
  st.metric(
      label='Số sinh viên đạt (>= 5.0)', value=f'{so_sv_dat}/{len(df)} sinh viên'
  )
with col2:
  st.metric(
      label='SV cao điểm nhất',
      value=f"{sv_cao_nhat['Ho_ten']} ({sv_cao_nhat['Tong_ket']} điểm)",
  )
  st.metric(
      label='SV thấp điểm nhất',
      value=f"{sv_thap_nhat['Ho_ten']} ({sv_thap_nhat['Tong_ket']} điểm)",
  )
# Thêm Selectbox tra cứu từng sinh viên (Theo yêu cầu đề bài)
st.subheader('🔍 Tra cứu thông tin sinh viên')
ten_sv = st.selectbox('Chọn một sinh viên:', df['Ho_ten'])
sv_duoc_chon = df[df['Ho_ten'] == ten_sv].iloc[0]
st.info(f"""
- **Họ và tên:** {sv_duoc_chon['Ho_ten']}
- **Điểm Chuyên cần:** {sv_duoc_chon['Chuyen_can']}
- **Điểm Giữa kỳ:** {sv_duoc_chon['Giua_ky']}
- **Điểm Cuối kỳ:** {sv_duoc_chon['Cuoi_ky']}
- **Điểm Tổng kết:** **{sv_duoc_chon['Tong_ket']}**
- **Xếp loại:** **{sv_duoc_chon['Xep_loai']}**
""")
# #4. TRỰC QUAN HÓA (Vẽ biểu đồ dạng ngang giống hình yêu cầu)
st.subheader('📈 Biểu đồ điểm tổng kết')
fig, ax = plt.subplots(figsize=(6, 4))
ten_sv_list = df['Ho_ten'][::-1]
diem_sv_list = df['Tong_ket'][::-1]
ax.barh(ten_sv_list, diem_sv_list, color='#5b9bd5', height=0.6)
ax.set_xlim(0, 10)
ax.set_xticks([0, 2.5, 5, 7.5, 10])
ax.set_xticklabels(['0', '2.5', '5', '7.5', '10'], color='gray')
ax.tick_params(axis='y', colors='gray')
for spine in ax.spines.values():
  spine.set_visible(False)
ax.tick_params(bottom=False, left=False)
st.pyplot(fig)
# Thông tin sinh viên thực hiện bài làm ở cuối trang
st.markdown('---')
st.caption(
    'Ứng dụng được thực hiện bởi: **[Lưu Nguyễn Minh Vũ]** - MSSV: **[034208008842]**'
)
