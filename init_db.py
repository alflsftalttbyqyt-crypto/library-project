import streamlit as st
import sqlite3
import base64

# إعداد الصفحة
st.set_page_config(page_title="المكتبة الذكية", layout="wide")

# CSS "النسف" لأي تنسيق سابق
st.markdown("""
    <style>
    /* إجبار الشريط الجانبي على أخذ كامل العرض وتنسيق موحد */
    [data-testid="stSidebar"] {
        text-align: left !important;
    }
    .custom-sidebar-container {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 20px !important;
        padding: 10px !important;
        background-color: transparent !important;
    }
    .custom-logo { 
        width: 110px !important; 
        height: 110px !important; 
        border-radius: 50% !important; 
        object-fit: cover !important; 
    }
    .custom-text-box h3 { 
        color: #bba14f !important; 
        margin: 0 !important; 
        font-size: 1.4em !important; 
        white-space: nowrap !important;
    }
    .custom-text-box hr { 
        margin: 5px 0 !important; 
        border-top: 2px solid #bba14f !important; 
    }
    .custom-text-box p { 
        margin: 0 !important; 
        font-size: 1em !important; 
        font-weight: bold !important; 
        white-space: nowrap !important;
    }
    .custom-location { 
        font-size: 0.85em !important; 
        color: #555 !important; 
    }
    </style>
""", unsafe_allow_html=True)

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
    except: return ""

with st.sidebar:
    img_data = get_image_base64("logo.png")
    
    # هيكل جديد كلياً
    st.markdown(f"""
        <div class="custom-sidebar-container">
            <img src="{img_data}" class="custom-logo">
            <div class="custom-text-box">
                <h3>L - O ❘ مكتبة الطلبة</h3>
                <hr>
                <p>Bibliothèque des Étudiants</p>
                <div class="custom-location">~ ERRACHIDIA ~</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("إضافة كتاب جديد")
    new_title = st.text_input("عنوان الكتاب")
    if st.button("إضافة"):
        if new_title:
            conn = sqlite3.connect("library.db")
            c = conn.cursor()
            c.execute("INSERT INTO books (title) VALUES (?)", (new_title,))
            conn.commit()
            conn.close()
            st.rerun()

st.title("المكتبة الذكية")