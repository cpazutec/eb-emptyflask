from flask import Flask
import os
import mysql.connector
from mysql.connector import Error

# print a nice greeting.
def say_hello(username = "World"):
 return '<p>Hello %s!</p>\n' % username

def connbd(bd1):
 msg = 'starting '
 if 'RDS_HOSTNAME' in os.environ:
  DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql','NAME': os.environ['RDS_DB_NAME'],'USER': os.environ['RDS_USERNAME'],'PASSWORD': os.environ['RDS_PASSWORD'],'HOST': os.environ['RDS_HOSTNAME'],'PORT': os.environ['RDS_PORT'],}}
  dbname = os.environ['RDS_DB_NAME']
  dbuser = os.environ['RDS_USERNAME']
  dbpwd = os.environ['RDS_PASSWORD']
  dbport = os.environ['RDS_PORT']
  dbhost = os.environ['RDS_HOSTNAME']
  try:
   connection = mysql.connector.connect(host=dbhost, database=dbname, user=dbuser, password=dbpwd)
   if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    msg = msg + '--> connected'
    print("You're connected to database: ", record)
  except Error as e:
   print("Error while connecting to MySQL", e)
  finally:
   if connection.is_connected():
    cursor.close()
    connection.close()
    msg = msg + ' --> closed'
    print("MySQL connection is closed")
 else:
  DATABASES = 'XX'
  dbname = 'nodb'
 return 'Hello '+bd1 + ' --> ' + msg

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))

application.add_url_rule('/<bd1>', 'hello', (lambda bd1: header_text +
    say_hello() + instructions + connbd(bd1) + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
