import sqlite3
import argparse

def search_book(title):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()
    
    # البحث عن الكتاب في الجدول
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + title + '%',))
    results = cursor.fetchall()
    
    if results:
        print("النتائج الموجودة:")
        for book in results:
            print(book)
    else:
        print("لم يتم العثور على كتب بهذا العنوان.")
        
    connection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", help="عنوان الكتاب للبحث عنه")
    args = parser.parse_args()
    if args.title:
        search_book(args.title)