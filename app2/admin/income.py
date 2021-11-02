from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Blueprint,render_template,url_for,request,redirect

Income = Blueprint('Income',__name__,static_folder='static',template_folder='templates')

client = MongoClient("mongodb+srv://shreyas:shreyas_070201@cluster0.1bktr.mongodb.net/networth?retryWrites=true&w=majority")
db = client.get_database('networth')
records3 = db.income

def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False


@Income.route('/income/<id>')
def income(id):
    rec_income = list(records3.find({'userID':id}))
    return render_template('inc.html',id=id,rec_income=rec_income)

@Income.route('/income0/<id>')
def income0(id):
    msg = 'Income Successfully Added'
    rec_income = list(records3.find({'userID':id}))
    return render_template('inc.html',id=id,rec_income=rec_income,msg=msg)

@Income.route('/income1/<id>')
def income1(id):
    msg1 = 'Name of the Asset is too long. Make sure name is under 20 characters.'
    rec_income = list(records3.find({'userID':id}))
    return render_template('inc.html',id=id,rec_income=rec_income,msg=msg1)

@Income.route('/income2/<id>')
def income2(id):
    msg2 =  'Name must contain atleast 1 alphabet.'
    rec_income = list(records3.find({'userID':id}))
    return render_template('inc.html',id=id,rec_income=rec_income,msg=msg2)

@Income.route('/income3/<id>')
def income3(id):
    msg3 = 'Enter integer or float value for cost.'
    rec_income = list(records3.find({'userID':id}))
    return render_template('inc.html',id=id,rec_income=rec_income,msg=msg3)

@Income.route('/income4/<id>')
def income4(id):
    msg4 = 'Enter integer or float value for bonus.'
    rec_income = list(records3.find({'userID':id}))
    return render_template('inc.html',id=id,rec_income=rec_income,msg=msg4)

@Income.route('/income5/<id>')
def income5(id):
    msg5 = 'Enter positive value for cost.'
    rec_income = list(records3.find({'userID':id}))
    return render_template('inc.html',id=id,rec_income=rec_income,msg=msg5)

@Income.route('/income6/<id>')
def income6(id):
    msg6 = 'Enter positive value for bonus.'
    rec_income = list(records3.find({'userID':id}))
    return render_template('inc.html',id=id,rec_income=rec_income,msg=msg6)

@Income.route('/income7/<id>')
def income7(id):
    msg7 = 'Income source of this name already exists !'
    rec_income = list(records3.find({'userID':id}))
    return render_template('inc.html',id=id,rec_income=rec_income,msg=msg7)

@Income.route('/income8/<id>')
def income8(id):
    msg8 = 'Income successfully removed.'
    rec_income = list(records3.find({'userID':id}))
    return render_template('inc.html',id=id,rec_income=rec_income,msg=msg8)

@Income.route('/income/add/<id>', methods = ['POST'])
def addincome(id):
    name = request.form['Income_Name']
    cost = request.form['Cost_Income']
    bonus = request.form['Growth']
    years = 0

    if(len(name) >= 20):
        return redirect(url_for('Income.income1',id=id))
    elif(any(i.isalpha() for i in name) == False):
        return redirect(url_for('Income.income2',id=id))
    elif(check_float(cost) == False):
        return redirect(url_for('Income.income3',id=id))
    elif(check_float(bonus) == False):
        return redirect(url_for('Income.income4',id=id))
    elif(float(cost) < 0):
        return redirect(url_for('Income.income5',id=id))
    elif(float(bonus) < 0):
        return redirect(url_for('Income.income6',id=id))
    else:
        total = float(cost) + ((float(bonus)/100)*float(cost)*years)
    new_doc = {
    'userID':id,
    'source': name,
    'annualincome': cost,
    'bonus': bonus,
    'years': years,
    'total': total
    }

    if records3.find_one({'userID':str(id),'source':name}):
        return redirect(url_for('Income.income7',id=id))
    else:
        records3.insert_one(new_doc)
    return redirect(url_for('Income.income0',id=id))

@Income.route('/income/remove/<id>/<objid>')
def removeincome(id,objid):
    records3.delete_one({'_id':ObjectId(objid)})
    return redirect(url_for('Income.income8',id=id))