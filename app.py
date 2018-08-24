from flask import Flask, request, redirect, url_for, render_template
from flask_mysqldb import MySQL
from flask_modus import Modus
from student import Student
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

modus = Modus(app) # method overriding.....gives you the ability to override the default method i.e post => patch

# students = []

def find_student(id):
    return [student for student in students if student.id == id][0] #list comprehension

@app.route('/') # localhost:3000/
def root(): # will redirect you to whatever the url is for a function called index
    return redirect(url_for('index')) # redirects you right to /students

@app.route('/students', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # new_student = Student(request.form['first_name'], request.form['last_name'])
        # students.append(new_student)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO students(first_name, last_name) VALUES(%s, %s)', (request.form['first_name'], request.form['last_name']))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        resultValue = cur.execute('SELECT * FROM students')
        if resultValue > 0:
            studentDetails = cur.fetchall()
            return render_template('index.html', students=studentDetails)
    return render_template('index.html')
     # first 'students' refers to a var in index.html

@app.route('/students/new')
def new():
    return render_template('new.html')

@app.route('/students/<int:id>', methods=['GET', 'PATCH', 'DELETE']) # this changes the id from a string to an int
def show(id):
    found_student = find_student(id)
    # from IPython import embed; embed()
    if request.method == 'PATCH':
        found_student.first_name = request.form['first_name']
        found_student.last_name = request.form['last_name']
        return redirect(url_for('index'))
    if request.method == 'DELETE':
        students.remove(found_student)
        return redirect(url_for('index'))
    return render_template('show.html', student=found_student)

@app.route('/students/<int:id>/edit')
def edit(id):
    found_student = find_student(id)
    return render_template('edit.html', student=found_student)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
