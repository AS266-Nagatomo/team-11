import sqlite3


if __name__ == "__main__":
    dbname = 'reading_record.db'
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    db = conn.cursor()

    db.execute('CREATE TABLE anime(id INTEGER PRIMARY KEY NOT NULL, title TEXT NOT NULL, reputation TEXT NOT NULL, datetime DATETIME, point INTEGER)')
    db.execute('CREATE TABLE nobel(id INTEGER PRIMARY KEY NOT NULL, title TEXT NOT NULL, reputation TEXT NOT NULL, datetime DATETIME, point INTEGER)')
    db.execute('CREATE TABLE movie(id INTEGER PRIMARY KEY NOT NULL, title TEXT NOT NULL, reputation TEXT NOT NULL, datetime DATETIME, point INTEGER)')
    
