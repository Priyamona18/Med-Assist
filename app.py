from flask import Flask, render_template, request, request, jsonify, session, redirect, url_for
import pickle
from datetime import datetime

# Load Model & Vectorizer
with open("chatbot_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

import sqlite3 as lite
conn = lite.connect('system.db')

app = Flask(__name__)
app.secret_key = 'health'


@app.route('/logout')
def logout():
	# remove the username from the session if it is there
    session.pop('susername', None)
    session.pop('sadminname', None)
    session.clear()
    return redirect(url_for('index'))


@app.route('/showSignUp', methods=['GET','POST'])
def showSignUp():
	if request.method == 'POST':
		username = request.form['uname']
		password = request.form['upass']
		email = request.form['uemail']
		pno = request.form['uphone']
		name = request.form['fname']
		
		
		#print username,password,email,pno,name,dob,address,adharno,rcno,gender,desig,fathername,city,district,job,monincome
		         
		conn = lite.connect('system.db')
		cursor = conn.cursor()
		cursor.execute("INSERT INTO reg (username,password,email,pno,name) VALUES('"+username+"','"+password+"','"+email+"','"+pno+"','"+name+"')")
		conn.commit()
		return redirect(url_for('index', registered='yes'))
	
	return render_template('signup.html')

@app.route('/appointment', methods=['GET','POST'])
def appointment():
    if request.method == 'POST':
        dname = request.form['dname']
        username=session['lname']
        adate = request.form['adate']
        apptime = request.form['atime']
        email = request.form['uemail']
        pno = request.form['uphone']
        reason = request.form['reason']
        
        conn = lite.connect('system.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO appointment (username,dname,adate,atime,email,pno,reason) VALUES('"+username+"','"+dname+"','"+adate+"','"+apptime+"','"+email+"','"+pno+"','"+reason+"')")
        conn.commit()
        return redirect(url_for('vappointment'))
    
    return render_template('appointment.html')   

@app.route('/vappointment1', methods=['GET','POST'])
def vappointment1():
    
    
    conn = lite.connect('system.db')
    cursor = conn.cursor()      
    cursor.execute("select username,dname,adate,atime,email,pno,reason from appointment")
    rows = cursor.fetchall()
        
    return render_template('vappointment.html', data = rows)
                    
@app.route('/vappointment', methods=['GET','POST'])
def vappointment():
    user=session['lname']
    conn = lite.connect('system.db')
    cursor = conn.cursor()      
    cursor.execute("select username,dname,adate,atime,email,pno,reason from appointment where username='"+user+"'")
    rows = cursor.fetchall()
        
    return render_template('vappointment.html', data = rows)

@app.route('/dashboard')
def dashboard():
	
	user=session['lname']
	conn = lite.connect('system.db')
	cursor = conn.cursor()		
	cursor.execute("select user,udate,query,answer from queries where user='"+user+"'")
	rows = cursor.fetchall()
		
	return render_template('dashboard.html', data = rows)

	
@app.route('/', methods=['GET','POST'])		
def index():
	if request.method == 'POST':
		uname = request.form['uname']
		upass = request.form['upass']
		
		conn = lite.connect('system.db')
		cursor = conn.cursor()
		cursor.execute("select COUNT(*),username,password from reg where username = '"+uname+"' and password='"+upass+"'")
		count = cursor.fetchone()[0]
    		
		if count > 0:
			session['susername']='user'
			sname=request.form['uname']
			session['lname']=sname
			return redirect(url_for('dashboard'))
			
		else: 
			return render_template('index.html')		

	return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"]
    user_input_vectorized = vectorizer.transform([user_input])
    response = model.predict(user_input_vectorized)[0]
    user=session['lname']
    current_datetime = datetime.now()
    udate = current_datetime.strftime('%Y-%m-%d %H:%M:%S')    
    conn = lite.connect('system.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO queries (user,udate,query,answer) VALUES('"+user+"','"+udate+"','"+user_input+"','"+response+"')")
    conn.commit()
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=False)

