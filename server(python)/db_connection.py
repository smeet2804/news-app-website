import psycopg2




class dbConnection():

   def getConnection(self):

      conn = psycopg2.connect(
         database="newsDB", user='postgres', password='smeet', host='127.0.0.1', port= '5432'
      )
      cursor = conn.cursor()

      cursor.execute("select version()")

      data = cursor.fetchone()
#      print("Connection established to: ",data)
      return cursor,conn