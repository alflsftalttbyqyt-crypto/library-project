import streamlit as st
import sqlite3
import os
import base64

# إعداد الصفحة
st.set_page_config(page_title="المكتبة الذكية - الراشيدية", layout="wide")

# إنشاء مجلد للكتب
if not os.path.exists("books_files"):
    os.makedirs("books_files")

# --- تهيئة قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, dept TEXT, sem TEXT, path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS extra_books 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, dept TEXT, sem TEXT, path TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- نظام الدخول الأكاديمي المعدل والصارم ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

if not st.session_state.logged_in:
    # دالة قراءة الصورة كخلفية وتنسيق واجهة الدخول
    def add_bg_and_styling(image_file):
        try:
            with open(image_file, "rb") as file:
                encoded_string = base64.b64encode(file.read()).decode()
            st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            * {{ direction: rtl; }}
            .block-container {{
                background-color: rgba(235, 225, 200, 0.95);
                border: 3px solid #6b4c1a;
                border-radius: 15px;
                padding: 40px;
                margin-top: 50px;
                box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.7);
                max-width: 600px;
            }}
            .stButton>button {{
                background-color: #4a3615;
                color: white;
                border-radius: 10px;
                border: 2px solid #2d4373;
                width: 100%;
                font-weight: bold;
                font-size: 18px;
                transition: 0.3s;
            }}
            .stButton>button:hover {{
                background-color: #6b4c1a;
                border-color: #bba14f;
            }}
            .email-suffix {{
                margin-top: 35px; 
                font-weight: bold; 
                color: #333;
                font-size: 16px;
            }}
            
            /* --- أكواد التجاوب مع شاشات الهواتف (لواجهة الدخول) --- */
            @media (max-width: 768px) {{
                .block-container {{
                    padding: 20px !important;
                    margin-top: 20px !important;
                    width: 95% !important;
                }}
                h2 {{
                    font-size: 1.5em !important;
                }}
                .email-suffix {{
                    margin-top: 5px !important;
                    text-align: center;
                    font-size: 14px;
                    margin-bottom: 15px;
                }}
            }}
            </style>
            """,
            unsafe_allow_html=True
            )
        except FileNotFoundError:
            st.error("⚠️ لم يتم العثور على صورة الخلفية! يرجى وضع صورة باسم bg.png في مجلد المشروع.")

    # استدعاء الخلفية والتصميم
    add_bg_and_styling('bg.png')

    st.markdown("<h2 style='text-align: center; color: #4a3615;'>🎓 بوابة الدخول الموحدة - لطلبة الرشيدية</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6b4c1a;'>Unified Entrance Portal - for Students of Errachidia</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        email_prefix = st.text_input("البريد الأكاديمي:", placeholder="يجب أن ينتهي بـ @edu.umi.ac.ma")
    with col2:
        st.markdown("<div class='email-suffix'>@edu.umi.ac.ma</div>", unsafe_allow_html=True)
    
    password = st.text_input("كلمة السر:", type="password", placeholder="أدخل كلمة المرور هنا...")
    
    st.write("---")
    
    # التوجيه للتواصل عبر فيسبوك
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px; padding: 10px;">
            لإضافة مواد أو كتب جديدة، يرجى التواصل معي عبر فيسبوك:<br>
            <a href="https://www.facebook.com/profile.php?id=100093495249631" target="_blank" style="font-weight: bold; color: #0056b3; text-decoration: none; font-size: 16px;">🔗 LAHCEN OUKHOUAOU</a>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("دخول"):
        if email_prefix and email_prefix.endswith("@edu.umi.ac.ma"):
            if password == "admin2024":
                st.session_state.logged_in = True
                st.session_state.is_admin = True
                st.rerun()
            elif password == "fpe2024":
                st.session_state.logged_in = True
                st.session_state.is_admin = False
                st.rerun()
            else:
                st.error("❌ كلمة السر غير صحيحة!")
        else:
            st.error("❌ عذراً، يجب أن ينتهي البريد الأكاديمي بـ @edu.umi.ac.ma")
    st.stop()

# --- التنسيق الجمالي (CSS) للمكتبة (بعد الدخول - متجاوب مع الهواتف) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Amiri&display=swap');
        
        .header-container { display: flex; justify-content: space-between; align-items: center; margin-top: -50px; margin-bottom: 30px; }
        .uthmani-text { font-family: 'Amiri', serif; font-size: 1.1em; color: #333; text-align: right; }
        .pray-text { margin-right: 50px; }
        .brand-text { font-size: 1.5em; font-weight: bold; color: #bba14f; }
        
        div[data-testid="stSelectbox"]:has(input[aria-label*="الشعبة"]) div[data-baseweb="select"] { border: 2px solid #2ecc71 !important; border-radius: 8px !important; }
        div[data-testid="stSelectbox"]:has(input[aria-label*="الفصل"]) div[data-baseweb="select"] { border: 2px solid #f1c40f !important; border-radius: 8px !important; }
        div[data-testid="stExpander"] { background-color: #f1c40f !important; border: none; }
        
        .welcome-box { background: linear-gradient(135deg, #bba14f, #d4af37); padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
        
        /* --- أكواد التجاوب مع شاشات الهواتف (للمكتبة من الداخل) --- */
        @media (max-width: 768px) {
            .header-container {
                flex-direction: column;
                text-align: center;
                margin-top: -20px;
            }
            .brand-text {
                margin-bottom: 15px;
            }
            .uthmani-text {
                text-align: center;
                font-size: 0.95em;
            }
            .pray-text {
                margin-right: 0 !important;
                display: block;
                margin-top: 8px;
            }
            .welcome-box {
                padding: 15px;
            }
            .welcome-box h2 {
                font-size: 1.3em !important;
            }
            .welcome-box p {
                font-size: 1em !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# --- الهيدر ---
st.markdown("""
    <div class="header-container">
        <div class="brand-text">ℒ - 𝒪</div>
        <div class="uthmani-text">
            بسم الله الرحمن الرحيم، الحمد لله الذي بنعمته تتم الصالحات.<br>
            <span class="pray-text">اللهم صل على سيدنا محمد وعلى آله وصحبه وسلم.</span>
        </div>
    </div>
""", unsafe_allow_html=True)

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
    except: return ""

departments = ["الفلسفة التطبيقية", "القانون (عام)", "القانون (خاص)", "الدراسات العربية", "الدراسات الإسلامية", "الدراسات الإنجليزية", "الدراسات الفرنسية", "الإقتصاد"]
semesters = ["S1", "S2", "S3", "S4", "S5", "S6"]

# --- الشريط الجانبي ---
with st.sidebar:
    img_data = get_image_base64("logo.png")
    st.markdown(f"""
        <div style="text-align: center;">
            <img src="{img_data}" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; max-width: 100%;">
            <div style="color: #bba14f; font-weight: bold; margin-top: 10px;">
                <div style="font-size: 1.2em;">L - O ❘ مكتبة الطلبة</div>
                <hr style="border-top: 2px solid #bba14f;">
                <div style="font-size: 0.9em; color: #333;">Bibliothèque des Étudiants</div>
                <div style="font-size: 0.8em; color: #666; margin-top: 5px;">~ ERRACHIDIA ~</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🔍 بحث خارجي (مكتبة نور)")
    noor_query = st.text_input("اسم الكتاب للبحث في نور:")
    if noor_query:
        st.link_button("ابحث في مكتبة نور ↗️", f"https://www.noor-book.com/books/search?query={noor_query}")
    
    st.markdown("---")
    
    if st.session_state.is_admin:
        st.subheader("إضافة مواد جديدة (خاص بالمدير)")
        selected_dept = st.selectbox("الشعبة:", departments)
        selected_sem = st.selectbox("الفصل:", semesters)
        
        st.subheader("PDF: رفع ملفات المواد")
        uploaded_files = st.file_uploader("اختر عدة ملفات:", type=["pdf"], accept_multiple_files=True)
        
        if st.button("حفظ الملفات"):
            if uploaded_files:
                conn = sqlite3.connect("library.db")
                c = conn.cursor()
                for uf in uploaded_files:
                    path = os.path.join("books_files", uf.name)
                    c.execute("SELECT id FROM books WHERE title = ? AND dept = ? AND sem = ?", (uf.name, selected_dept, selected_sem))
                    if not c.fetchone():
                        with open(path, "wb") as f: f.write(uf.getbuffer())
                        c.execute("INSERT INTO books (title, dept, sem, path) VALUES (?, ?, ?, ?)", (uf.name, selected_dept, selected_sem, path))
                conn.commit(); conn.close(); st.success("تم الحفظ!"); st.rerun()

        st.markdown("---")
        st.subheader("إضافة كتبك الخاصة:")
        private_pdfs = st.file_uploader("اختر كتبك:", type=["pdf"], accept_multiple_files=True)
        
        if st.button("حفظ الكتب الخاصة"):
            if private_pdfs:
                conn = sqlite3.connect("library.db")
                c = conn.cursor()
                for p_pdf in private_pdfs:
                    path = os.path.join("books_files", p_pdf.name)
                    with open(path, "wb") as f: f.write(p_pdf.getbuffer())
                    c.execute("INSERT INTO books (title, dept, sem, path) VALUES (?, ?, ?, ?)", (p_pdf.name, selected_dept, selected_sem, path))
                conn.commit(); conn.close(); st.success("تم الحفظ!"); st.rerun()
    else:
        st.info("تصفح المكتبة متاح. لإضافة كتب تواصل مع الإدارة.")

# --- التصميم الترحيبي ---
st.markdown("""
    <div class="welcome-box">
        <h2 style="margin: 0; font-family: 'Amiri', serif;">Azul imhdar n imteɣren ❘ مرحبا بطلبة الرشيدية</h2>
        <p style="margin: 15px 0 0; font-size: 1.2em; line-height: 1.6;">
            بوابة معرفية مفتوحة للجميع، تتضمن موارد ومصادر تعليمية متنوعة. تم تصميم هذا المحتوى خصيصاً لدعم طلبة الكلية متعددة التخصصات بالرشيدية في مسيرتهم الأكاديمية. لا تترددوا في الاستفادة منها.<br>
            <br><strong>_FPE Errachidia</strong>
        </p>
    </div>
""", unsafe_allow_html=True)

# --- عرض المكتبة والتحميل للزوار ---
filter_dept = st.selectbox("تصفح حسب الشعبة:", departments)

for sem in semesters:
    with st.expander(f"المواد الخاصة بـ {sem}"):
        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        c.execute("SELECT title, path FROM books WHERE dept = ? AND sem = ?", (filter_dept, sem))
        books = c.fetchall()
        conn.close()
        
        cols = st.columns(4) 
        for i, book in enumerate(books):
            with cols[i % 4]:
                # تقصير اسم الملف الطويل ليناسب التصميم
                short_title = book[0][:15] + "..." if len(book[0]) > 15 else book[0]
                st.write(f"📖 {short_title}")
                
                # قراءة الملف بشكل آمن وعرض زر التحميل (متاح للجميع)
                try:
                    with open(book[1], "rb") as f:
                        pdf_data = f.read()
                    st.download_button(
                        label="تحميل", 
                        data=pdf_data, 
                        file_name=os.path.basename(book[1]), 
                        mime='application/pdf', 
                        key=f"d_{sem}_{i}"
                    )
                except FileNotFoundError:
                    st.error("⚠️ الملف غير متوفر")
        
        # تعبئة الفراغات إذا كان عدد الكتب لا يقبل القسمة على 4
        for i in range(len(books), (len(books) + (4 - len(books) % 4)) if len(books) % 4 != 0 else len(books)):
            if len(books) == 0:
                break
            with cols[i % 4]: st.write("")
        if len(books) == 0:
            st.info("لا توجد ملفات في هذا الفصل حالياً.")

# --- الكتب الإضافية ---
st.markdown("---")
st.subheader("✨ مكتبة المراجع والمصادر الإثرائية ✨")

if st.session_state.is_admin:
    uploaded_extras = st.file_uploader("اسحب وأفلت ملفات المراجع هنا (خاص بالمدير):", type=["pdf"], accept_multiple_files=True, key="extra_general")

    if st.button("حفظ المراجع المختارة"):
        if uploaded_extras:
            conn = sqlite3.connect("library.db")
            c = conn.cursor()
            for up_ex in uploaded_extras:
                f_path = os.path.join("books_files", up_ex.name)
                with open(f_path, "wb") as f: f.write(up_ex.getbuffer())
                c.execute("INSERT INTO extra_books (title, dept, sem, path) VALUES (?, ?, ?, ?)", (up_ex.name, filter_dept, "عام", f_path))
            conn.commit(); conn.close(); st.success("تم إضافة المراجع بنجاح!"); st.rerun()

conn = sqlite3.connect("library.db")
c = conn.cursor()
c.execute("SELECT title, path FROM extra_books WHERE dept = ?", (filter_dept,))
extra_books = c.fetchall()
conn.close()

if extra_books:
    for i, eb in enumerate(extra_books):
        col_text, col_btn = st.columns([4, 1])
        with col_text:
            st.write(f"📁 {eb[0]}")
        with col_btn:
            try:
                with open(eb[1], "rb") as f:
                    extra_data = f.read()
                st.download_button(
                    label="تحميل",
                    data=extra_data,
                    file_name=os.path.basename(eb[1]),
                    mime='application/pdf',
                    key=f"extra_d_{i}"
                )
            except FileNotFoundError:
                st.error("غير متوفر")
else:
    st.info("لا توجد مراجع إضافية مضافة بعد.")

# --- التذييل ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; font-family: sans-serif; color: #333; padding: 20px;">
        <div style="font-size: 1.1em; margin-bottom: 10px;">للمزيد من المساعدة والشرح أو تساؤل تواصل معي، لا تتردد في الضغط على الاسم</div>
        <div style="margin: 5px 0;">
            <a href="https://www.facebook.com/profile.php?id=100093495249631" style="font-weight: bold; color: #007bff; text-decoration: none; font-size: 1.2em;">LAHCEN OUKHOUAOU</a>
        </div>
        <div style="font-size: 35px; line-height: 1.5; background: linear-gradient(to bottom, blue, green, yellow); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">ⵣ</div>
    </div>
""", unsafe_allow_html=True)