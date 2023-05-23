from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import timedelta
import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(512).hex()
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'calendar'
app.config['MYSQL_PASSWORD'] = 'XXXXXXXXXXXXXXXXXX'
app.config['MYSQL_DB'] = 'calendar'
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



@app.route('/api/leaveday', methods=['POST'])
def check_leaveday():

    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        leaveday = data.get('leaveday')

        # Kiểm tra định dạng ngày
        if is_valid_date(leaveday):
            if write_leaveday("username", leaveday):
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'error', 'message': 'User already registered for the given date'})
        else:
            return jsonify({'status': 'error'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

def is_valid_date(date_string):
    try:
        # Kiểm tra định dạng ngày
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def write_leaveday(username,leaveday):
    color = session['colors']
    try:
        # Đọc dữ liệu hiện có từ tệp tin JSON
        with open('leavedays.json', 'r') as file:
            data = json.load(file)

        for item in data:
            if item["username"] == session['username'] and item["start"] == leaveday:
                return False
        # Thêm thông tin mới vào danh sách
        data.append({
            "title": "fullname",
            "color": color,
            "start": leaveday,
            "username": session['username']
        })

        # Ghi lại dữ liệu vào tệp tin JSON
        with open('leavedays.json', 'w') as file:
            json.dump(data, file)
        return True
    except Exception as e:
        print('Error writing leaveday:', str(e))

@app.route('/leavedays')
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    # You'd normally use the variables above to limit the data returned
    # you don't want to return ALL events like in this code
    # but since no db or any real storage is implemented I'm just
    # returning data from a text file that contains json elements

    with open("leavedays.json", "r") as input_data:
        # you should use something else here than just plaintext
        # check out jsonfiy method or the built in json module
        # http://flask.pocoo.org/docs/0.10/api/#module-flask.json
        return input_data.read()

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
        if username is not None:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user['userid']
            session['username'] = user['username']
            session['colors'] = str(user['colors'])
            # Redirect to calendar page
            return redirect(url_for('leaving'))
        else:
            # Account doesnt exist or username/password incorrect
            flash('Sai tên đăng nhập hoặc mật khẩu')
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0')