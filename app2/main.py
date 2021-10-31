from flask import Flask,render_template,url_for,redirect,request
import math,random
from flask_mail import Mail,Message
from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib

from admin.login import login 
from admin.register import register
from admin.home import Home
from admin.assets import Asset
from admin.liabilities import Liability
from admin.income import Income
from admin.expenditure import Expenditure

app = Flask(__name__)
app.register_blueprint(login,url_prefix='/admin')
app.register_blueprint(register,url_prefix='/admin')
app.register_blueprint(Home,url_prefix='/admin')
app.register_blueprint(Asset,url_prefix='/admin')
app.register_blueprint(Liability,url_prefix='/admin')
app.register_blueprint(Income,url_prefix='/admin')
app.register_blueprint(Expenditure,url_prefix='/admin')

client = MongoClient("mongodb+srv://shreyas:shreyas_070201@cluster0.1bktr.mongodb.net/networth?retryWrites=true&w=majority")
db = client.get_database('networth')
records = db.networth
records6 = db.otp 

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'worthit070201@gmail.com'
app.config['MAIL_PASSWORD'] = 'WorthIT@070201'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

def Hash(user_entered_password):
    salt = "5gz"
    db_password = user_entered_password+salt
    h = hashlib.md5(db_password.encode())
    return h.hexdigest()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgetpassword.html')

@app.route('/generateotp/<username>',methods=['GET','POST'])
def generateotp(username):
    if request.method == 'POST':
        rec = list(records6.find({'username':username}))
        num = rec[0]['otp']
        email = rec[0]['email']
        subject = 'Your OTP is ' + str(num)

        message = Message(subject,sender='worthit070201@gmail.com',recipients=[email])
        message.body = subject

        mail.send(message)
        
@app.route('/email',methods=['POST'])
def email():
    username = request.form['username']
    rec = list(records.find({'username':username}))
    if rec:
        id = rec[0]['_id']
        num  = math.floor(random.random()*1000000)
        if(len(list(records6.find({'username':username}))) == 0):
            new_doc = {
                'userID': id,
                'username': username,
                'email': rec[0]['email'],
                'otp': num
            }
            records6.insert(new_doc)
            rec1 = list(records6.find({'username':username}))
        else:
            records6.update({'username':username},{"$set":{ 'otp':num }})
            rec1 = list(records6.find({'username':username}))
        user = rec[0]['username']
        generateotp(user)  
        id1 = rec1[0]['_id']
        return render_template('otp.html',id1=id1)
    else:
        msg = 'Invalid username'
        return render_template('forgetpassword.html',msg=msg)

@app.route('/otp/<id1>', methods =['GET','POST'])
def otp(id1):
    if request.method == 'POST':
        Otp = request.form['otp']
        rec = list(records6.find({'_id':ObjectId(id1)}))
        num = rec[0]['otp']
        rec1 = list(records.find({'username':rec[0]['username']}))
        id = rec1[0]['_id']
        if(int(Otp) == int(num)):
            return render_template('changepassword.html',id=id)
        else:
            msg1 = "Incorrect OTP";
            return render_template('otp.html',msg1=msg1)

@app.route('/changepassword/<id>', methods=['GET','POST'])
def changepassword(id):
    if request.method == 'POST':
        password = request.form['Password']
        confirm = request.form['confirm']
        if (str(password) == str(confirm)):
            records.update({'_id':ObjectId(id)},{"$set": { 'password':Hash(password) }})
            msg1 = 'Password Successfully Changed !!!'
            return render_template('login.html',msg1=msg1)
        else:
            msg = 'Passwords do not match'
            return render_template('changepassword.html',id=id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)