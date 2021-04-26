from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
import re
import csv

app = Flask(__name__)

todo_list = [
    ("Buy Eggs", "a@gmail.com", "High"),
    ("Get Vaccine", "b@gmail.com", "High"),
    ("Watch TV", "a@gmail.com", "Low"),
]

@app.route('/')
def display_list():

    return render_template('todo.html', todo_list=todo_list)

@app.route('/submit', methods=["POST"])

def submit():
    global todo_list
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    #email format validation
    rex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    if (re.search(rex, email)):
       todo_list.append((task, email, priority))
       return redirect(url_for('display_list'))
    else:
        return redirect(url_for('display_list'))

@app.route('/save')
def save():
    #export the current todo list as csv

    global todo_list
    with open('todo_list', 'w') as f:

        write = csv.writer(f)
        write.writerows(todo_list)

    return redirect(url_for('display_list'))

@app.route('/clear')
def clear():
    #create a clear button on the webpage
    global todo_list
    todo_list = []
    return redirect(url_for('display_list'))

@app.route('/delete', methods = ["POST"])
def delete():
    #delete record base on the index number

    global todo_list
    index = request.form['delete']

    todo_list.pop(int(index)-1)
    return redirect(url_for('display_list'))

if __name__ == '__main__':
    app.run(debug=True)
