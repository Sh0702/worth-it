from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Blueprint,render_template,url_for,request,redirect

Asset = Blueprint('Asset',__name__,static_folder='static',template_folder='templates')

client = MongoClient("mongodb+srv://shreyas:shreyas_070201@cluster0.1bktr.mongodb.net/networth?retryWrites=true&w=majority")
db = client.get_database('networth')
records1 = db.assets

def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False


@Asset.route('/asset/<id>')
def asset(id):
    rec_asset = list(records1.find({'userID':id}))
    return render_template('asset.html',id=id,rec_asset=rec_asset)

@Asset.route('/asset1/<id>')
def asset1(id):
    msg1 = 'Asset successfully added !!!'
    rec_asset = list(records1.find({'userID':id}))
    return render_template('asset.html',id=id,rec_asset=rec_asset,msg=msg1)

@Asset.route('/asset2/<id>')
def asset2(id):
    msg2 = 'Name of the Asset is too long. Please make name less than 20 characters.'
    rec_asset = list(records1.find({'userID':id}))
    return render_template('asset.html',id=id,rec_asset=rec_asset,msg=msg2)

@Asset.route('/asset3/<id>')
def asset3(id):
    msg3 = 'Name must contain atleast 1 alphabet.'
    rec_asset = list(records1.find({'userID':id}))
    return render_template('asset.html',id=id,rec_asset=rec_asset,msg=msg3)

@Asset.route('/asset4/<id>')
def asset4(id):
    msg4 = 'Enter integer or float value for cost.'
    rec_asset = list(records1.find({'userID':id}))
    return render_template('asset.html',id=id,rec_asset=rec_asset,msg=msg4)

@Asset.route('/asset5/<id>')
def asset5(id):
    msg5 = 'Enter integer or float value for growth percentage.'
    rec_asset = list(records1.find({'userID':id}))
    return render_template('asset.html',id=id,rec_asset=rec_asset,msg=msg5)

@Asset.route('/asset6/<id>')
def asset6(id):
    msg6 = 'Enter positive value for cost.'
    rec_asset = list(records1.find({'userID':id}))
    return render_template('asset.html',id=id,rec_asset=rec_asset,msg=msg6)

@Asset.route('/asset7/<id>')
def asset7(id):
    msg7 = 'Enter positive value for growth percentage.'
    rec_asset = list(records1.find({'userID':id}))
    return render_template('asset.html',id=id,rec_asset=rec_asset,msg=msg7)

@Asset.route('/asset8/<id>')
def asset8(id):
    msg8 = 'Asset with this name already exists !'
    rec_asset = list(records1.find({'userID':id}))
    return render_template('asset.html',id=id,rec_asset=rec_asset,msg=msg8)

@Asset.route('/asset9/<id>')
def asset9(id):
    msg9 = 'Asset successfully removed !'
    rec_asset = list(records1.find({'userID':id}))
    return render_template('asset.html',id=id,rec_asset=rec_asset,msg=msg9)

@Asset.route('/assets/add/<id>', methods = ['POST'])
def addasset(id):
    name = request.form['Assets']
    cost = request.form['Cost_asset']
    type = request.form['Asset Type']
    if(type == "-1"):
        gp = request.form['Other']
        gp = float(gp)/100
    else:
        gp = float(type)

    if(len(name) >= 20):
        return redirect(url_for('Asset.asset2',id=id))
    elif(any(i.isalpha() for i in name) == False):
        return redirect(url_for('Asset.asset3',id=id))
    elif(check_float(cost) == False):
        return redirect(url_for('Asset.asset4',id=id))
    elif(check_float(gp) == False):
        return redirect(url_for('Asset.asset5',id=id))
    elif(float(cost) < 0):
        return redirect(url_for('Asset.asset6',id=id))
    elif(float(gp) < 0):
        return redirect(url_for('Asset.asset7',id=id))
    else:
        new_doc = {
            'userID': id,
            'assetname': name,
            'assetvalue': cost,
            'growth_percentage': gp,
            'total': 1,
            'years': 1
            }
    
    if(records1.find_one({'userID':str(id),'assetname':name})):
        return redirect(url_for('Asset.asset8',id=id))
    else:
        records1.insert(new_doc)
    return redirect(url_for('Asset.asset1',id=id))

@Asset.route('/assets/remove/<id>/<objid>')
def removeasset(id,objid):
    records1.delete_one({'_id':ObjectId(objid)})
    return redirect(url_for('Asset.asset9',id=id))
    