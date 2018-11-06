from flask import Flask, render_template, request, redirect, flash
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = 'lololol'

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route("/")
def index():
    mysql = connectToMySQL('email')
    emails = mysql.query_db('SELECT * FROM email')
    
    return render_template('index.html', emails=emails)

@app.route("/create_email", methods=["POST"])
def validate_and_create_email():
  email = request.form['email']
  if not EMAIL_REGEX.match(email):
      flash(u"Invalid Email Address", 'fail')
      return redirect('/')
  else:
      mysql = connectToMySQL('email')
      query = 'INSERT INTO email (email) VALUES (%(e)s)'
      data = {'e': email}
      new_email_id = mysql.query_db(query, data)
      flash(u"Email successfully created", 'success')
      return redirect('/')


if __name__ =='__main__':
    app.run(debug=True)
