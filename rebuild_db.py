import streamlit as st
import sqlite3
import os
import base64

# إعداد الصفحة
st.set_page_config(page_title="المكتبة الذكية", layout="wide")

# إنشاء مجلد للكتب
if not os.path.exists("books_files"): os.makedirs("books_files")

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
    except: return ""

def init_db():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, dept TEXT, sem TEXT, path TEXT)''')
    conn.commit()
    conn.close()
init_db()

departments = ["الفلسفة التطبيقية", "القانون (عام)", "القانون (خاص)", "الدراسات العربية", "الدراسات الإسلامية", "الدراسات الإنجليزية", "الدراسات الفرنسية", "الإقتصاد"]
semesters = ["S1", "S2", "S3", "S4", "S5", "S6"]

# --- الشريط الجانبي (التصميم) ---
with st.sidebar:
    img_data = get_image_base64("logo.png")
    st.markdown(f"""
        <div style="text-align: center;">
            <img src="{img_data}" style="width: 140px; height: 140px; border-radius: 50%; object-fit: cover;">
            <div style="color: #bba14f; font-weight: bold; margin-top: 10px;">
                <div style="font-size: 1.2em;">L - O ❘ مكتبة الطلبة</div>
                <hr style="border-top: 2px solid #bba14f;">
                <div style="font-size: 0.9em; color: #333;">Bibliothèque des Étudiants</div>
                <div style="font-size: 0.8em; color: #666; margin-top: 5px;">~ ERRACHIDIA ~</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("إضافة مواد جديدة")
    selected_dept = st.selectbox("الشعبة:", departments)
    selected_sem = st.selectbox("الفصل:", semesters)
    # هنا التعديل للسماح برفع 7 ملفات دفعة واحدة
    uploaded_files = st.file_uploader("اختر حتى 7 ملفات PDF:", type=["pdf"], accept_multiple_files=True)
    
    if st.button("حفظ الملفات"):
        if uploaded_files:
            conn = sqlite3.connect("library.db")
            c = conn.cursor()
            for uploaded_file in uploaded_files:
                file_path = os.path.join("books_files", uploaded_file.name)
                with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
                c.execute("INSERT INTO books (title, dept, sem, path) VALUES (?, ?, ?, ?)", 
                          (uploaded_file.name, selected_dept, selected_sem, file_path))
            conn.commit()
            conn.close()
            st.success("تم الحفظ!")
            st.rerun()

# --- التصميم الترحيبي ---
st.markdown("""
    <div style="background: linear-gradient(90deg, #bba14f, #f4ecd0); padding: 25px; border-radius: 20px; color: #333; text-align: center; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h1 style="margin: 0; font-family: sans-serif;">مرحباً بكم في فضاء L-O للمعرفة</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.1em;">بوابة الطلبة والباحثين في رحاب مدينة الرشيدية - جسركم الرقمي نحو المراجع المتميزة.</p>
    </div>
""", unsafe_allow_html=True)

# --- عرض المكتبة ---
st.header("تصفح المراجع العلمية")
filter_dept = st.selectbox("تصفح حسب الشعبة:", departments)

for sem in semesters:
    with st.expander(f"المواد الخاصة بـ {sem}"):
        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        c.execute("SELECT title, path FROM books WHERE dept = ? AND sem = ?", (filter_dept, sem))
        books = c.fetchall()
        conn.close()
        
        cols = st.columns(7)
        for i in range(7):
            with cols[i]:
                if i < len(books):
                    st.write(f"📖 {books[i][0][:10]}...")
                    with open(books[i][1], "rb") as f:
                        st.download_button("تحميل", f, file_name=os.path.basename(books[i][1]), key=f"d_{sem}_{i}")
                else:
                    st.info("فارغ")