from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Blueprint,render_template,url_for,request,redirect

Liability = Blueprint('Liability',__name__,static_folder='static',template_folder='templates')

client = MongoClient("mongodb+srv://shreyas:shreyas_070201@cluster0.1bktr.mongodb.net/networth?retryWrites=true&w=majority")
db = client.get_database('networth')
records2 = db.liabilities

def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False

@Liability.route('/liability/<id>')
def liability(id):
    rec_liability = list(records2.find({'userID':id}))
    return render_template('liabilities.html',id=id,rec_liability=rec_liability)

@Liability.route('/liability0/<id>')
def liability0(id):
    msg = 'Liability successfully added'
    rec_liability = list(records2.find({'userID':id}))
    return render_template('liabilities.html',id=id,rec_liability=rec_liability,msg=msg)

@Liability.route('/liability1/<id>')
def liability1(id):
    msg1 = 'Name of the Liability is too long. Please make name less than 20 characters.'
    rec_liability = list(records2.find({'userID':id}))
    return render_template('liabilities.html',id=id,rec_liability=rec_liability,msg=msg1)

@Liability.route('/liability2/<id>')
def liability2(id):
    msg2 =  'Name must contain atleast 1 alphabet.'
    rec_liability = list(records2.find({'userID':id}))
    return render_template('liabilities.html',id=id,rec_liability=rec_liability,msg=msg2)

@Liability.route('/liability3/<id>')
def liability3(id):
    msg3 = 'Enter integer or float value for cost.'
    rec_liability = list(records2.find({'userID':id}))
    return render_template('liabilities.html',id=id,rec_liability=rec_liability,msg=msg3)

@Liability.route('/liability4/<id>')
def liability4(id):
    msg4 = 'Enter integer or float value for growth percentage.'
    rec_liability = list(records2.find({'userID':id}))
    return render_template('liabilities.html',id=id,rec_liability=rec_liability,msg=msg4)

@Liability.route('/liability5/<id>')
def liability5(id):
    msg5 = 'Enter integer or float value for growth percentage.'
    rec_liability = list(records2.find({'userID':id}))
    return render_template('liabilities.html',id=id,rec_liability=rec_liability,msg=msg5)

@Liability.route('/liability6/<id>')
def liability6(id):
    msg6 = 'Enter positive value for Liabilities Value.'
    rec_liability = list(records2.find({'userID':id}))
    return render_template('liabilities.html',id=id,rec_liability=rec_liability,msg=msg6)

@Liability.route('/liability7/<id>')
def liability7(id):
    msg7 = 'Enter positive value for Liabilities Value.'
    rec_liability = list(records2.find({'userID':id}))
    return render_template('liabilities.html',id=id,rec_liability=rec_liability,msg=msg7)

@Liability.route('/liability8/<id>')
def liability8(id):
    msg8 = 'Enter positive value for growth percentage.'
    rec_liability = list(records2.find({'userID':id}))
    return render_template('liabilities.html',id=id,rec_liability=rec_liability,msg=msg8)

@Liability.route('/liability9/<id>')
def liability9(id):
    msg9 = 'Liability name already exists !'
    rec_liability = list(records2.find({'userID':id}))
    return render_template('liabilities.html',id=id,rec_liability=rec_liability,msg=msg9)

@Liability.route('/liability10/<id>')
def liability10(id):
    msg10 = 'Liability successfully removed !'
    rec_liability = list(records2.find({'userID':id}))
    return render_template('liabilities.html',id=id,rec_liability=rec_liability,msg=msg10)

@Liability.route('/liabilities/add/<id>', methods = ['POST'])
def addliability(id):
    name = request.form['Liabilities']
    cost = request.form['Cost_liabilities']
    emi = request.form['emi']
    interest = request.form['Percentage_Interest']
    years = 0

    if(len(name) >= 20):
        return redirect(url_for('Liability.liability1',id=id))
    elif(any(i.isalpha() for i in name) == False):
        return redirect(url_for('Liability.liability2',id=id))
    elif(check_float(cost) == False):
        return redirect(url_for('Liability.liability3',id=id))
    elif(check_float(emi) == False):
        return redirect(url_for('Liability.liability4',id=id))
    elif(check_float(interest) == False):
        return redirect(url_for('Liability.liability5',id=id))
    elif(float(cost) < 0):
        return redirect(url_for('Liability.liability6',id=id))
    elif(float(emi) < 0):
        return redirect(url_for('Liability.liability7',id=id))
    elif(float(interest) < 0):
        return redirect(url_for('Liability.liability8',id=id))
    else:
        total = float(cost)*((1 + float(interest))**years)
    new_doc = {
    'userID':id,
    'liabilitiesname': name,
    'Principleamt': cost,
    'interest': float(interest),
    'annualamt': emi,
    'years': years,
    'total': total
    }
    
    if records2.find_one({'userID':str(id),'liabilitiesname':name}):
        return redirect(url_for('Liability.liability9',id=id))
    else:
        records2.insert_one(new_doc)
    return redirect(url_for('Liability.liability0',id=id))

@Liability.route('/liabilities/remove/<id>/<objid>')
def removeliability(id,objid):
    records2.delete_one({'_id':ObjectId(objid)})
    return redirect(url_for('Liability.liability10',id=id))
