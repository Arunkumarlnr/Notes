from flask import Flask, flash, render_template, request, session, redirect, url_for, escape


from flaskext.mysql import MySQL
app=Flask(__name__)
app.secret_key = 'note'

mysql = MySQL(app)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'note'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

    
    				
@app.route('/', methods=['GET','POST'])		
def index():
	if request.method == 'POST':
		title = request.form['title']
		description = request.form['description']
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("INSERT INTO details (title,description)VALUES('"+title+"','"+description+"')")
		conn.commit()
		return redirect(url_for('viewurl'))
		
		
	return render_template('index.html')
	
@app.route('/viewurl')
def viewurl():
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("select title,description,nid from details")
		rows = cursor.fetchall()
		return render_template('viewurl.html', data = rows)

@app.route('/delnote/<nid>', methods=['GET','POST'])
def delnote_entry(nid):
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("delete from details where nid ='"+nid+"'")
		conn.commit()
		return redirect(url_for('viewurl'))
		
		
@app.route('/editnote/<nid>', methods=['GET','POST'])
def editnote_entry(nid):
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("select title,description,nid from details where nid='"+nid+"'")
			rows = cursor.fetchall()
			return render_template('editnote.html', data = rows) 
				
@app.route('/updatenote', methods=['GET','POST'])
def updatenote_entry():
	if request.method == 'POST':
		nid = request.form['nid']
		title = request.form['title']
		description = request.form['description']
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("update details set title='"+title+"',description='"+description+"' where nid='"+nid+"'")
		conn.commit()
		return redirect(url_for('viewurl'))
		
		
	return render_template('viewurl.html')
			
			
if __name__=="__main__":
	app.debug = True
	app.run()
	app.run(debug = True)
