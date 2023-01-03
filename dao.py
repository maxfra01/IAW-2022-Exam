import sqlite3

def get_all_categories():
   conn=sqlite3.connect('db/podcast.db')
   conn.row_factory = sqlite3.Row
   cursor=conn.cursor()
   
   sql='SELECT DISTINCT category FROM serie ORDER BY category'
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

def get_user_by_email(email):
   conn=sqlite3.connect('db/podcast.db')
   conn.row_factory = sqlite3.Row
   cursor=conn.cursor()
   sql='SELECT * FROM utenti WHERE email=?'
   cursor.execute(sql, (email, ))
   user=cursor.fetchone()
   
   cursor.close()
   conn.close()
   return user

def get_user_by_id(user_id):
   conn=sqlite3.connect('db/podcast.db')
   conn.row_factory = sqlite3.Row
   cursor=conn.cursor()
   sql='SELECT * FROM utenti WHERE id=?'
   cursor.execute(sql, (user_id, ))
   user=cursor.fetchone()
   
   cursor.close()
   conn.close()
   return user


def add_user(new_user):
   conn=sqlite3.connect('db/podcast.db')
   conn.row_factory = sqlite3.Row
   cursor=conn.cursor()
   success=False
   
   sql='INSERT INTO utenti(email, password, name, surname, type) VALUES (?,?,?,?,?)'
 
   try:
      cursor.execute(sql, (new_user['email'], new_user['password'], new_user['name'], new_user["surname"], new_user["type"]))
      conn.commit()
      success = True
   except Exception as e:
      print('ERROR', str(e))
      conn.rollback()

   cursor.close()
   conn.close()
   
   return success

def get_show_by_id(id):
   conn=sqlite3.connect('db/podcast.db')
   conn.row_factory = sqlite3.Row
   cursor=conn.cursor()
   sql='SELECT * FROM serie WHERE id=?'
   cursor.execute(sql, (id, ))
   serie=cursor.fetchone()
   
   cursor.close()
   conn.close()
   return serie

def get_episodes_by_showid(show_id):
   conn=sqlite3.connect('db/podcast.db')
   conn.row_factory = sqlite3.Row
   cursor=conn.cursor()
   sql='SELECT * FROM episodio WHERE show_id=? ORDER BY date'
   cursor.execute(sql, (show_id, ))
   episodi=cursor.fetchall()
   
   cursor.close()
   conn.close()
   return episodi


def add_show(new_show):
   conn=sqlite3.connect('db/podcast.db')
   conn.row_factory = sqlite3.Row
   cursor=conn.cursor()
   success=False
   
   sql='INSERT INTO serie(title, category, image, creator_id, description, creator_name) VALUES (?,?,?,?,?,?)'
 
   try:
      cursor.execute(sql, (new_show['title'], new_show['category'], new_show['image'], new_show['description'], new_show["creator_id"], new_show["creator_name"]))
      conn.commit()
      success = True
   except Exception as e:
      print('ERROR', str(e))
      conn.rollback()

   cursor.close()
   conn.close()
   
   return success

def get_my_show(creator_id):
   conn=sqlite3.connect('db/podcast.db')
   conn.row_factory = sqlite3.Row
   cursor=conn.cursor()
   
   sql='SELECT * FROM serie WHERE creator_id=?'
   cursor.execute(sql, (creator_id, ))
   shows=cursor.fetchall()
   
   cursor.close()
   conn.close()
   return shows