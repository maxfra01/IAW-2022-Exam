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

def get_user_by_email(email,type):
   conn=sqlite3.connect('db/podcast.db')
   conn.row_factory = sqlite3.Row
   cursor=conn.cursor()
   if type=='creatore':
      sql='SELECT * FROM creatore WHERE email=?'
   else:
      sql='SELECT * FROM ascoltatore WHERE email=?'
   cursor.execute(sql, (email, ))
   user=cursor.fetchone()
   
   cursor.close()
   conn.close()
   return user

def add_user(new_user):
   conn=sqlite3.connect('db/podcast.db')
   conn.row_factory = sqlite3.Row
   cursor=conn.cursor()
   success=False
   
   if new_user["tipo"]=='creatore':
      sql='INSERT INTO creatore(email, password, name) VALUES (?,?,?)'
   else:
      sql='INSERT INTO ascoltatore(email, password, name) VALUES (?,?,?)'
   try:
      cursor.execute(sql, (new_user['email'], new_user['password'], new_user['name']))
      conn.commit()
      success = True
   except Exception as e:
      print('ERROR', str(e))
      conn.rollback()

   cursor.close()
   conn.close()
   
   return success