import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- Cấu hình trang Streamlit ---
st.set_page_config(
    page_title="Trợ lý Chấm Toán AI",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS tùy chỉnh để làm đẹp giao diện ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        border-color: #ff3333;
    }
    h1 {
        color: #1f77b4;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar: Cấu hình API ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3771/3771278.png", width=100)
    st.title("Cấu hình hệ thống")
    st.markdown("---")
    
    api_key = st.text_input(
        "Nhập Google API Key 🔑", 
        type="password", 
        help="Lấy API Key tại https://aistudio.google.com/"
    )
    
    st.info("""
    **Hướng dẫn:**
    1. Nhập API Key của bạn.
    2. Tải lên ảnh chụp bài toán.
    3. Nhấn 'Chấm bài ngay' để AI phân tích.
    """)
    st.markdown("---")
    st.caption("Powered by Gemini 1.5 Flash & Streamlit")

# --- Giao diện chính ---
col1, col2 = st.columns([1, 2])

with col1:
    st.title("🧮 Chấm Toán AI")
    st.markdown("**Trợ lý học tập thông minh dành cho học sinh**")
    
    uploaded_file = st.file_uploader("Tải ảnh bài làm (JPG, PNG)...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Hiển thị ảnh đã tải lên
        image = Image.open(uploaded_file)
        st.image(image, caption="Bài làm của học sinh", use_column_width=True)
    else:
        st.info("Vui lòng tải lên hình ảnh để bắt đầu.")

with col2:
    st.header("📝 Kết quả chấm bài")
    
    # Nút bấm xử lý
    analyze_button = st.button("🚀 CHẤM BÀI NGAY")

    if analyze_button:
        if not api_key:
            st.error("⚠️ Vui lòng nhập Google API Key ở thanh bên trái (Sidebar) để tiếp tục.")
        elif not uploaded_file:
            st.warning("⚠️ Vui lòng tải lên hình ảnh bài tập trước khi chấm.")
        else:
            try:
                with st.spinner("🤖 AI đang đọc bài và chấm điểm... Vui lòng đợi trong giây lát!"):
                    # Cấu hình Gemini
                    genai.configure(api_key=api_key)
                    
                    # Cấu hình Model (Sử dụng 1.5 Flash cho tốc độ và chi phí tối ưu)
                    model = genai.GenerativeModel('gemini-1.5-flash')

                    # Prompt (Câu lệnh) cho AI - Đóng vai giáo viên
                    prompt = """
                    Bạn là một giáo viên Toán học tận tâm, thân thiện và có trình độ sư phạm cao.
                    Hãy xem hình ảnh đính kèm (là bài tập về nhà của học sinh) và thực hiện các nhiệm vụ sau:

                    1. **Nhận diện bài toán:** Viết lại đề bài mà bạn nhìn thấy trong ảnh để xác nhận.
                    2. **Kiểm tra từng bước:** Dò xét kỹ lưỡng từng bước giải của học sinh.
                    3. **Chấm điểm & Nhận xét:**
                       - Nếu đúng: Khen ngợi và giải thích ngắn gọn tại sao đúng.
                       - Nếu sai: Chỉ ra chính xác lỗi sai nằm ở bước nào (ví dụ: tính toán sai, áp dụng sai công thức).
                    4. **Lời giải đúng:** Cung cấp lời giải chi tiết, chính xác từng bước để học sinh tham khảo.
                    5. **Đánh giá:** Chấm điểm trên thang điểm 10.

                    **Yêu cầu định dạng:** Trình bày kết quả bằng Markdown đẹp mắt, sử dụng các công thức toán học LaTeX (dạng $...$) nếu cần thiết. Giọng văn khuyến khích, tích cực.
                    """

                    # Gọi API
                    response = model.generate_content([prompt, image])
                    
                    # Hiển thị kết quả
                    st.success("Đã chấm xong! Dưới đây là kết quả chi tiết:")
                    st.markdown(response.text)
                    
            except Exception as e:
                st.error(f"Đã xảy ra lỗi trong quá trình xử lý: {str(e)}")
                st.markdown("Gợi ý: Kiểm tra lại API Key hoặc chất lượng hình ảnh.")

# --- Footer ---
st.markdown("---")
st.markdown("<center>Phát triển bởi Chuyên gia EdTech | 2024</center>", unsafe_allow_html=True)