from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Blueprint,render_template,url_for,request,redirect

Expenditure = Blueprint('Expenditure',__name__,static_folder='static',template_folder='templates')

client = MongoClient("mongodb+srv://shreyas:shreyas_070201@cluster0.1bktr.mongodb.net/networth?retryWrites=true&w=majority")
db = client.get_database('networth')
records4 = db.expenditure

def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False

def check_int(potential_int):
    try:
        int(potential_int)
        return True
    except ValueError:
        return False

@Expenditure.route('/expenditure/<id>')
def expenditure(id):
    rec_expenditure = list(records4.find({'userID':id}))
    return render_template('expenditure.html',id=id,rec_expenditure = rec_expenditure)

@Expenditure.route('/expenditure0/<id>')
def expenditure0(id):
    msg = 'Expenditure Successfully Added'
    rec_expenditure = list(records4.find({'userID':id}))
    return render_template('expenditure.html',id=id,rec_expenditure = rec_expenditure,msg=msg)

@Expenditure.route('/expenditure1/<id>')
def expenditure1(id):
    msg1 = 'Name of the Asset is too long.'
    rec_expenditure = list(records4.find({'userID':id}))
    return render_template('expenditure.html',id=id,rec_expenditure = rec_expenditure,msg=msg1)

@Expenditure.route('/expenditure2/<id>')
def expenditure2(id):
    msg2 =  'Name must contain atleast 1 alphabet.'
    rec_expenditure = list(records4.find({'userID':id}))
    return render_template('expenditure.html',id=id,rec_expenditure = rec_expenditure,msg=msg2)

@Expenditure.route('/expenditure3/<id>')
def expenditure3(id):
    msg3 = 'Enter integer or float value for cost.'
    rec_expenditure = list(records4.find({'userID':id}))
    return render_template('expenditure.html',id=id,rec_expenditure = rec_expenditure,msg=msg3)

@Expenditure.route('/expenditure4/<id>')
def expenditure4(id):
    msg4 = 'Enter integer or float value for growth percentage.'
    rec_expenditure = list(records4.find({'userID':id}))
    return render_template('expenditure.html',id=id,rec_expenditure = rec_expenditure,msg=msg4)

@Expenditure.route('/expenditure5/<id>')
def expenditure5(id):
    msg5 = 'Enter integer or float value for growth percentage.'
    rec_expenditure = list(records4.find({'userID':id}))
    return render_template('expenditure.html',id=id,rec_expenditure = rec_expenditure,msg=msg5)

@Expenditure.route('/expenditure6/<id>')
def expenditure6(id):
    msg6 = 'Enter positive value for cost.'
    rec_expenditure = list(records4.find({'userID':id}))
    return render_template('expenditure.html',id=id,rec_expenditure = rec_expenditure,msg=msg6)

@Expenditure.route('/expenditure7/<id>')
def expenditure7(id):
    msg7 = 'Enter positive value for growth percentage.'
    rec_expenditure = list(records4.find({'userID':id}))
    return render_template('expenditure.html',id=id,rec_expenditure = rec_expenditure,msg=msg7)

@Expenditure.route('/expenditure8/<id>')
def expenditure8(id):
    msg8 = 'Enter positive value for years.'
    rec_expenditure = list(records4.find({'userID':id}))
    return render_template('expenditure.html',id=id,rec_expenditure = rec_expenditure,msg=msg8)

@Expenditure.route('/expenditure9/<id>')
def expenditure9(id):
    msg9 = 'Expenditure of this name already exists !'
    rec_expenditure = list(records4.find({'userID':id}))
    return render_template('expenditure.html',id=id,rec_expenditure = rec_expenditure,msg=msg9)

@Expenditure.route('/expenditure10/<id>')
def expenditure10(id):
    msg10 = 'Expenditure Successfully removed.'
    rec_expenditure = list(records4.find({'userID':id}))
    return render_template('expenditure.html',id=id,rec_expenditure = rec_expenditure,msg=msg10)

@Expenditure.route('/expenditure/add/<id>', methods = ['POST'])
def addexpenditure(id):
    name = request.form['Expenditure_Name']
    cost = request.form['Expenditure_Value']
    growth = request.form['Growth']
    years = request.form['Number_years']

    if(len(name) >= 20):
        return redirect(url_for('Expenditure.expenditure1',id=id))
    elif(any(i.isalpha() for i in name) == False):
        return redirect(url_for('Expenditure.expenditure2',id=id))
    elif(check_float(cost) == False):
        return redirect(url_for('Expenditure.expenditure3',id=id))
    elif(check_float(growth) == False):
        return redirect(url_for('Expenditure.expenditure4',id=id))
    elif(check_int(years) == False):
        return redirect(url_for('Expenditure.expenditure5',id=id))
    elif(float(cost) < 0):
        return redirect(url_for('Expenditure.expenditure6',id=id))
    elif(float(growth) < 0):
        return redirect(url_for('Expenditure.expenditure7',id=id))
    elif(int(years) < 0 or int(years) > 5):
        return redirect(url_for('Expenditure.expenditure8',id=id))
    else:
        total = float(cost) + ((float(growth)/100) * float(cost) * int(years))
    new_doc = {
        'userID':id,
        'type': name,
        'cost': cost,
        'growth': growth,
        'years': years,
        'total': total
    }

    if records4.find_one({'userID':str(id),'type':name}):
        return redirect(url_for('Expenditure.expenditure9',id=id))
    else:
        records4.insert_one(new_doc)
    return redirect(url_for('Expenditure.expenditure0',id=id))

@Expenditure.route('/expenditure/remove/<id>/<objid>')
def removeexpenditure(id,objid):
    records4.delete_one({'_id':ObjectId(objid)})
    return redirect(url_for('Expenditure.expenditure10',id=id))