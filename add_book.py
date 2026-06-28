import sqlite3

def add_book(title, author, category):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    # إضافة الكتاب
    cursor.execute("INSERT INTO books (title) VALUES (?)", (title,))
    conn.commit()
    conn.close()
    print(f"تم إضافة الكتاب '{title}' بنجاح!")

# تجربة إضافة كتاب
add_book("نقد العقل المحض", "إيمانويل كانط", "فلسفة")