from flask import Flask, render_template, render_template_string, request, redirect, url_for, session
from flask_mysqldb import MySQL
import hashlib, secrets
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


app.secret_key = 'a'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'selva2002'
app.config['MYSQL_DB'] = 'haus'
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/builderinfo', methods=['GET', 'POST'])
def builderinfo():
    msg = ''
    name = ''
    if 'register' in request.form:
        if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'confirm-password' in request.form and 'companyname' in request.form and 'industry' in request.form and 'location' in request.form and 'phone' in request.form:
            username = request.form['name']
            email = request.form['email']
            password = request.form['password']
            conpassword = request.form['confirm-password']
            companyname = request.form['companyname']
            industry = request.form['industry']
            location = request.form['location']
            phone = request.form['phone']
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            hashed_conpassword = hashlib.sha256(conpassword.encode()).hexdigest()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM builder WHERE username = % s', (username, ))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers !'
            elif not username or not password or not email:
                msg = 'Please fill out the form !'
            else:
                if (password == conpassword):
                    cursor.execute('INSERT INTO builder VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, %s)', (username, email, hashed_password, hashed_conpassword, companyname, industry, location, phone))
                    mysql.connection.commit()
                    msg = 'Dear %s You have successfully registered !'%(username)
                else:
                    msg = 'Passwords does not match.Re-enter password'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template('builderlogin.html', msg=msg)
    else:
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            username = request.form['email']
            password = request.form['password']
            hashpass = hashlib.sha256(password.encode()).hexdigest()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM builder WHERE email = %s AND hashed_password = % s', (username, hashpass))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['username'] = username
                msg = "Login successful"
                return render_template('dashboard.html',name = username)
            else:
                msg = "Invalid Credentials"
        return render_template('Builderlogin.html',msg = msg)

@app.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    msg = ''
    name = ''
    if 'register' in request.form:
        if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'confirm-password' in request.form and 'location' in request.form and 'phone' in request.form:
            username = request.form['name']
            email = request.form['email']
            password = request.form['password']
            conpassword = request.form['confirm-password']
            location = request.form['location']
            phone = request.form['phone']
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            hashed_conpassword = hashlib.sha256(conpassword.encode()).hexdigest()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers !'
            elif not username or not password or not email:
                msg = 'Please fill out the form !'
            else:
                if (password == conpassword):
                    cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s, % s, % s, %s)', (username, email, hashed_password, hashed_conpassword, location, phone))
                    mysql.connection.commit()
                    msg = 'Dear %s You have successfully registered !'%(username)
                else:
                    msg = 'Passwords does not match.Re-enter password'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template('builderlogin.html', msg=msg)
    else:
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            username = request.form['email']
            password = request.form['password']
            hashpass = hashlib.sha256(password.encode()).hexdigest()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE email = %s AND hashed_password = % s', (username, hashpass))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['username'] = username
                msg = "Login successful"
                return render_template('dashboard.html',name = username)
            else:
                msg = "Invalid Credentials"
        return render_template('userlogin.html',msg = msg)
        

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('builderinfo'))

@app.route('/loggout')
def loggout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('userinfo'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
