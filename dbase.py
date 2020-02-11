import sqlite3

class DB():
  
  def __init__(self):
    self.conn = sqlite3.connect('states.db')
    self.c = self.conn.cursor()
    self.c.execute(''' CREATE TABLE IF NOT EXISTS state (id integer primary key, key text, value text)''')

    self.c.execute(''' CREATE TABLE IF NOT EXISTS file_paths( id integer primary key,chat_id text, audio_path text, image_path text) ''')
    self.conn.commit()
   


  
    

  def set_state(self, key, value):
    with sqlite3.connect('states.db') as con:
      cursor = con.cursor()
      cursor.execute(''' SELECT value FROM state WHERE key =? ''',(key,))
    
      ex_result = cursor.fetchall()
    
      if len(ex_result) == 0:
        cursor.execute(''' INSERT INTO state (key, value) values(?, ?) ''', (key, value))
        con.commit()
      elif len(ex_result) == 1:
        cursor.execute(''' UPDATE state SET value = ? WHERE key = ? ''',(value, key))
        con.commit()

    return True    


  def get_state(self , key):
      with sqlite3.connect('states.db') as con:
          cursor = con.cursor()
          cursor.execute(''' SELECT value FROM state WHERE key = ? ''',(key,))  
          ex_result = cursor.fetchall() 
     
          if len(ex_result) == 1:
              return ex_result[0][0]
    
  def set_path_value(self, field, value, chat_id):
      chat_id = str(chat_id)
      count = 0
      with sqlite3.connect('states.db') as con:
          cursor = con.cursor()
          cursor.execute(" SELECT {} FROM file_paths WHERE chat_id = ? ".format(field),(chat_id,))
          result = cursor.fetchone()

          if result :
              if result[0]:
                  count = len(result[0].split(','))
                  value = '{},{}'.format(result[0], value)
              cursor.execute("UPDATE file_paths SET {} = ? WHERE chat_id = ?".format(field), (value, chat_id))
          else:
              cursor.execute( "INSERT INTO file_paths (chat_id,{}) values(?,?)".format(field), (chat_id, value))
          con.commit()

      return count+1, value


  def get_message_count(self, field, chat_id):
      chat_id = str(chat_id)
      with sqlite3.connect('states.db') as con:
          cursor = con.cursor()
          cursor.execute(" SELECT {} FROM file_paths WHERE chat_id = ? ".format(field),(chat_id,))
          result = cursor.fetchone()
      
          con.commit()
          if not result or not result[0]:
              return 0

      return len(result[0].split(','))


  def get_image_names(self, chat_id):
      chat_id = str(chat_id)

      with sqlite3.connect('states.db') as con:
          cursor = con.cursor()
          print('akdfjakl')
          cursor.execute(" SELECT image_path FROM file_paths WHERE chat_id = ? ", (chat_id,))
          print('kkkkkkkkkkkkkkkkkkk')
          result = cursor.fetchone()
          print(result)
          if result and result[0] != None:
              return result[0]


