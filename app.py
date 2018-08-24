from flask import Flask, request, redirect, url_for, render_template
from student import Student

app = Flask(__name__)

students = []

def find_student(id):
    return [student for student in students if student.id == id][0] #list comprehension

@app.route('/') # localhost:3000/
def root(): # will redirect you to whatever the url is for a function called index
    return redirect(url_for('index')) # redirects you right to /students

@app.route('/students', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_student = Student(request.form['first_name'], request.form['last_name'])
        students.append(new_student)
        return redirect(url_for('index'))
    return render_template('index.html', students=students) # first 'students' refers to a var in index.html

@app.route('/students/new')
def new():
    return render_template('new.html')

@app.route('/students/<int:id>') # this changes the id from a string to an int
def show(id):
    found_student = find_student(id)
    # for student in students:
    #     if(student.id == id):
    #         found_student = student
    return render_template('show.html', student=found_student)

@app.route('/students/<int:id>/edit')
def edit(id):
    found_student = find_student(id)
    return render_template('edit.html', student=found_student)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
