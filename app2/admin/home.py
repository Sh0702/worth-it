from flask import Blueprint,render_template,request,redirect,url_for
from pymongo import MongoClient

client = MongoClient("mongodb+srv://shreyas:shreyas_070201@cluster0.1bktr.mongodb.net/networth?retryWrites=true&w=majority")
db = client.get_database('networth')
records = db.networth #login
records1 = db.assets
records2 = db.liabilities
records3 = db.income
records4 = db.expenditure
records5 = db.total

Home = Blueprint('Home',__name__,static_folder='static',template_folder='templates')

@Home.route('/homepage/<id>')
def home(id):
    return render_template('home.html',id=id)

@Home.route('/homepage/display/<id>')
def home2(id):
    print(list(records5.find({'userID':id})))
    rec_display = list(records5.find({'userID':id}))
    return render_template('home.html',id=id,rec_display=rec_display)

@Home.route('/homepage/<id>/<msg>')
def home3(id,msg):
    return render_template('home.html',id=id,msg=msg)

@Home.route('/homepage/update/<id>', methods = ['POST'])
def update(id):
    y = request.form['Years']
    years = int(y)
    records1.update_many({'userID':id},{"$set": {'years':years}})
    records2.update_many({'userID':id},{"$set": {'years':years}})
    records3.update_many({'userID':id},{"$set": {'years':years}})
    rec1 = list(records1.find({'userID':id}))
    rec2 = list(records2.find({'userID':id}))
    rec3 = list(records3.find({'userID':id}))
    rec4 = list(records4.find({'userID':id}))
    for i in rec1:
        base = (1 + (float(i['growth_percentage']) * 0.01))
        total = (float(i['assetvalue']) * (pow(base,int(i['years']))))
        records1.update_one({'userID': str(id),'assetname':i['assetname']},{'$set':{'total':total}})
    for i in rec2:
        total = float(i['Principleamt']) 
        print(total)
        if(years != 0):
            t = years*12
            for j in range(t):
                if(total > 0):
                    total = (total * (1 + float(i['interest'])/1200)) - float(i['annualamt'])
                else:
                    total = 0
                    break
        records2.update_one({'userID':str(id),'liabilitiesname':i['liabilitiesname']},{'$set':{'total':total}})
    for i in rec3:
        total = float(i['annualincome']) + (float(i['annualincome']) * float(i['bonus']) * int(i['years'])/100)
        records3.update_one({'userID':str(id),'source':i['source']},{'$set':{'total':total}})
    for i in rec4:
        if(int(i['years']) < years):
            total = float(i['cost']) + (float(i['cost']) * float(i['growth']) * int(i['years'])/100)
        else:
            total = float(i['cost']) + ((float(i['cost']) * float(i['growth']) * years)/100)
        records4.update_one({'userID':str(id),'type':i['type']},{'$set':{'total':total}})
    assettotal = 0
    liabilitytotal = 0
    incometotal = 0
    expendituretotal = 0
    rec1 = list(records1.find({'userID':id}))
    rec2 = list(records2.find({'userID':id}))
    rec3 = list(records3.find({'userID':id}))
    rec4 = list(records4.find({'userID':id}))
    for i in rec1:
        assettotal += i['total']
    for i in rec2:
        liabilitytotal += i['total']
    for i in rec3:
        incometotal += i['total']
    for i in rec4:
        expendituretotal += i['total']
    Networth = assettotal + incometotal - expendituretotal - liabilitytotal
    new_doc = {
        'userID':id,
        'years': years,
        'assettotal':round(assettotal,2),
        'incometotal':round(incometotal,2),
        'expendituretotal': round(expendituretotal,2),
        'liabilitytotal': round(liabilitytotal,2),
        'networth': round(Networth,2)
    }
    if list(records5.find({'userID':str(id)})):
        records5.update({'userID':id},{"$set":{'years': years,'assettotal':round(assettotal,2),'incometotal': round(incometotal,2),
        'expendituretotal': round(expendituretotal,2),'liabilitytotal': round(liabilitytotal,2),'networth': round(Networth,2)}})
    else:
        records5.insert(new_doc)
    msg = 'Updates Successful !!!'
    return redirect(url_for('Home.home3',id=id,msg=msg))

@Home.route('/homepage/go/<id>')
def go(id):
    return redirect(url_for('Home.home2',id=id))