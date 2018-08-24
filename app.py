from flask import Flask, request, redirect, url_for, render_template
from student import Student

app = Flask(__name__)

students = []

@app.route('/') # localhost:3000/
def root(): # will redirect you to whatever the url is for a function called index
    return redirect(url_for('index'))

@app.route('/students', methods=['GET', 'POST'])
    def index():
        return render_template('index.html', students=students) # first 'students' refers to a var in index.html

if __name__ == '__main__':
    app.run(debug=True, port=3000)
