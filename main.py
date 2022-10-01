from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)

app.secret_key = "12345654321"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "mydb"

mysql = MySQL(app)


@app.route('/')
def index():
    return redirect(url_for('home_page'))


@app.route('/index')
def home_page():
    return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Student WHERE email=%s and pass=%s", (email, password))
        info = cursor.fetchone()
        if info is not None:
            if info['email'] == email and info['pass'] == password:
                return render_template("index.html", logininfo="Hey,Your Login is SuccessFull !!")
        else:
            return render_template("Login.html", logininfo="You Entered wrong details, Please Enter valid Details !!")
    return render_template("login.html")


@app.route('/signup', methods=['POST', 'GET'])
def singup_page():
    if request.method == 'POST':
        if 'email' in request.form and 'createpassword' in request.form:
            email = request.form['email']
            password = request.form['createpassword']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("insert into Student (email,pass) values (%s, %s)", (email, password))
            mysql.connection.commit()
            return render_template("index.html", logininfo="Your Sign up is SuccessFulL !! Please Login for more !")
    return render_template("signup.html")



if __name__ == '__main__':
    app.run(debug=True)
