from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['student_db']
students_collection = db['students']

@app.route('/')
def index():
    students = students_collection.find()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        students_collection.insert_one({'name': name, 'age': age})
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/edit/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = students_collection.find_one({'_id': student_id})
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        students_collection.update_one(
            {'_id': student_id},
            {'$set': {'name': name, 'age': age}}
        )
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student, student_id=student_id)

@app.route('/delete/<student_id>')
def delete_student(student_id):
    students_collection.delete_one({'_id': student_id})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
