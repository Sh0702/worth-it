from flask import Blueprint,render_template,request
from pymongo import MongoClient
import hashlib

client = MongoClient("mongodb+srv://shreyas:shreyas_070201@cluster0.1bktr.mongodb.net/networth?retryWrites=true&w=majority")
db = client.get_database('networth')
records = db.networth #login

login = Blueprint('login',__name__,static_folder='static',template_folder='templates')

def Hash(user_entered_password):
    salt = "5gz"
    db_password = user_entered_password+salt
    h = hashlib.md5(db_password.encode())
    return h.hexdigest()

@login.route('/login', methods =['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    rec = records.find_one({'username':username,'password':Hash(password)})
    if rec:
        return render_template('home.html',id = rec['_id'])
    msg = 'Incorrect username or password !'
    return render_template('login.html',msg=msg)