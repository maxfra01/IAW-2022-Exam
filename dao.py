import sqlite3

def get_all_categories():
   conn=sqlite3.connect('db/podcast.db')
   conn.row_factory = sqlite3.Row
   cursor=conn.cursor()
   
   sql='SELECT DISTINCT category FROM serie'
   cursor.execute(sql)
   categories=cursor.fetchall()
   
   cursor.close()
   conn.close()
   return categories

def get_all_shows():
   conn=sqlite3.connect('db/podcast.db')
   conn.row_factory = sqlite3.Row
   cursor=conn.cursor()
   
   sql='SELECT * FROM serie'
   cursor.execute(sql)
   shows=cursor.fetchall()
   
   cursor.close()
   conn.close()
   return shows

   

   