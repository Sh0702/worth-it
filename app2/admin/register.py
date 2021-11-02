from flask import Blueprint,render_template,request
import re
from pymongo import MongoClient
import hashlib

client = MongoClient("mongodb+srv://shreyas:shreyas_070201@cluster0.1bktr.mongodb.net/networth?retryWrites=true&w=majority")
db = client.get_database('networth')
records = db.networth #login

register = Blueprint('Register',__name__,static_folder='static',template_folder='templates')
specialchar= ['@','#','$','%','^','&','*','?','/','|','~',':',';','!']

def check_name(x):
    for i in x:
        if(i.isalpha() == True or i == ''):
            return 1
        else:
            return 0

def Hash(user_entered_password):
    salt = "5gz"
    db_password = user_entered_password+salt
    h = hashlib.md5(db_password.encode())
    return h.hexdigest()

def letters(x):
    y = ''
    for i in x:
        if(i.isalpha() == True):
            y += i
    return y

@register.route("/createaccount")
def create():
    return render_template('signup.html')

@register.route('/register', methods =['POST'])
def insert():
    fullName = request.form['name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm']
    new_doc = {
    'name': fullName,
    'email': email,
    'username': username,
    'password': Hash(password)
    }
    if not username or not password or not email or not fullName:
        msg = 'Please fill out the form !'
    elif(check_name(fullName) == 0):
        msg1 = 'Name can only contain alphabetical characters and spaces.'
        return render_template('signup.html',msg=msg1)
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        msg2 = 'Invalid email address !'
        return render_template('signup.html',msg=msg2)
    elif records.find_one({'email':email}):
        msg3 = 'Account under this email ID already exists'
        return render_template('signup.html',msg=msg3)
    elif records.find_one({'username':username}):
        msg4 = 'Account already exists !'
        return render_template('signup.html',msg=msg4)
    elif((len(password) < 8) or (len(password) > 20)):
        msg5 = 'Please make your password size from 8 to 20 characters.'
        return render_template('signup.html',msg=msg5)
    elif(all(i.isupper() == False for i in letters(password)) or ((any(i.isalpha() for i in password) == False) or (any(i.isnumeric() for i in password) == False) or (any(i in specialchar for i in password) == False))):
        msg6 = 'Weak password'
        return render_template('signup.html',msg=msg6)
    elif password != confirm:
        msg7 = 'Passwords do not match.'
        return render_template('signup.html',msg=msg7)
    else:
        msg = 'Successfully Registered!!!'
        records.insert_one(new_doc)
        return render_template('login.html',msg=msg)