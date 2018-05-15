from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from flask import session
from flask import flash
import yaml
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

Bootstrap(app)


db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['SECRET_KEY'] = os.urandom(20)

@app.route('/')
def index():
    cur =  mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM new_users")
    if (result_value > 0):
        data = cur.fetchall()
        return render_template('index.html', data=data)


@app.route('/newuser/', methods = ['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        form = request.form
        name =  form['name']
        password = form['age']
        cur =  mysql.connection.cursor()
        cur.execute("INSERT INTO new_users(name, password) VALUES(%s, %s)",(name, password))
        mysql.connection.commit()
        flash('Database inserted successfully')
    return render_template('newuser.html')

# Display All users from database
@app.route('/allusers/')
def allusers():
    cur =  mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM new_users")
    if (result_value > 0):
        data = cur.fetchall()
        return render_template('allusers.html', data=data)

@app.route('/delete/<int:id>/')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM new_users WHERE id={}".format(id))
    mysql.connection.commit()
    return redirect('/allusers')

@app.route('/edit/<int:id>/', methods=['GET','POST'])
def edit(id):
    # Edit the data in the html columns
    if (request.method == 'POST'):
        cur = mysql.connection.cursor()
        name = request.form['name']
        password = request.form['password']
        cur.execute("UPDATE new_users SET name={}, password={} WHERE id={}".format(name,password,id))
        mysql.connection.commit()
        cur.close()
        return redirect('/allusers/')
    # View all data from the data into the column
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT name,password FROM new_users WHERE id={}".format(id))
    if (result_value > 0):
        data = cur.fetchone()
        form = {}
        form['name'] = data['name']
        form['password'] = data['password']
        cur.close()
        return render_template('edit.html', form=form)
















if __name__ == '__main__':
    app.run(debug=True)
