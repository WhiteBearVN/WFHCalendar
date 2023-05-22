from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import timedelta
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
mysql = MySQL(app)

@app.route("/leaving",methods=['GET'])
def leaving():
    if 'loggedin' in session:
           # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE userid = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('leaveoffice.html', account=account)
    return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND user_password = md5(%s)', (username, password,))
        user = cursor.fetchone()
        # If account exists in accounts table in out database
        if user is not None:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user['userid']
            session['username'] = user['username']
            session['colors'] = str(user['colors'])
            # Redirect to calendar page
            return redirect(url_for('index.html'))
        else:
            # Account doesnt exist or username/password incorrect
            flash('Sai tên đăng nhập hoặc mật khẩu')
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0')