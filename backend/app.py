from flask import Flask, request, jsonify
import pymongo
from fractions import Fraction
from flask_cors import CORS

import json
app = Flask(__name__)
CORS(app)

myclient = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0-o08tg.mongodb.net/test?retryWrites=true&w=majority")
database = myclient["MicaDatabase"]
groups = database["Groups"]

with open("../bankingAPI/getbanktransactions.json") as json_file:
    API_data = json.load(json_file)

@app.route('/')
def hello():
    return "Hello World!"

#will require the url to have the correct format where the username and password are passed in the url
#e.g http://127.0.0.1:5000/login?username=username&password=password
#returns true or false depending if the username and password were correct
#may need change
@app.route('/login', methods=["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    if username == "username" and password == "password":
        return jsonify(True)
    else:
        return jsonify(False)

#returns the getbanktransactions.json
@app.route('/get_personal_trans', methods=["GET"])
def get_personal_trans():
    return jsonify(API_data)

#will require the url to have the correct format where the groupID is passed in the url
#e.g http://127.0.0.1:5000/login?groupID=1
#returns a list of all transactions within the group
@app.route('/get_shared_trans', methods=["GET"])
def get_shared_trans():
    groupID = request.args.get("groupID")
    result = []
    group = groups.find_one({"groupID": str(groupID)})
    for trans in group["transactions"].values():
        result.append(trans)
    result = sorted(result, key = lambda i: i['postingDateTime'],reverse=True)
    print(sorted(result, key = lambda i: i['postingDateTime'],reverse=True))
    return jsonify(result)

#will require the url to have the correct format where the groupID is passed in the url
#e.g http://127.0.0.1:5000/login?groupID=1
#returns a list of all users within the group
@app.route('/get_users', methods=["GET"])
def get_users():
    groupID = request.args.get("groupID")
    result = []
    group = groups.find_one({"groupID": str(groupID)})
    for user in group["users"]:
        result.append(user)
    return jsonify(result)

#will require a json object to be passed
#e.g
# {
#    method: "POST",
#    headers: {
#        'Accept': 'application/json',
#        'Content-Type': 'application/json'
#    },
#    body: JSON.stringify({ "transaction": {<transaction data>}, "groupID": 1 })
#}
#can be used to add new transaction or change existing transaction with the same transaction ID
#returns true or false depending if the transaction was added/updated
@app.route('/put_trans', methods=["PUT"])
def put_trans():
    data = request.get_json()
    transaction = data['transaction']
    groupID = data['groupID']
    field = "transactions." + str(transaction["transactionID"])
    return jsonify(groups.update({"groupID": str(groupID)}, {'$set': {field: transaction}})["updatedExisting"])

#will require a json object to be passed
#e.g
# {
#    method: "POST",
#    headers: {
#        'Accept': 'application/json',
#        'Content-Type': 'application/json'
#    },
#    body: JSON.stringify({ "rule": "rule", "groupID": 1 })
#}
#returns true or false depending if the rule was added
@app.route('/put_rule', methods=["PUT"])
def put_rule():
    data = request.get_json()
    rule = data['rule']
    groupID = data['groupID']
    return jsonify(groups.update({"groupID": str(groupID)}, {'$push': {"rules": rule}})["updatedExisting"])

#will require the url to have the correct format where the groupID is passed in the url
#e.g http://127.0.0.1:5000/get_rules?groupID=1
#returns a list of all the rules
@app.route('/get_rules', methods=["GET"])
def get_rules():
    groupID = request.args.get("groupID")
    return jsonify(groups.find_one({"groupID": str(groupID)})["rules"])

#will require the url to have the correct format where the groupID is passed in the url
#e.g http://127.0.0.1:5000/get_total?groupID=1
#returns a dict with the names of all members, each member has another dict with names of all other members with a value corresponding to how much the member owes
#e.g
#{
#   "Bianca": { "John": 10, "Bill": 20},     ///Bianca owes John $10 and Bill $20
#   "John": { "Bianca": -10, "Bill": 30},     ///John owes Bianca -$10 (Bianca owes John $10) and Bill $30
#   "Bill": { "John": -30, "Bianca": -20},     ///Bill owes John -$30 (John owes Bill $30) and Bianca -$20 (Bianca owes John $20)
# }
@app.route('/get_total', methods=["GET"])
def get_total():
    result = {}
    groupID = request.args.get("groupID")
    group = groups.find_one({"groupID": str(groupID)})
    for user in group["users"]:
        result[user] = {}
        for i in group["users"]:
            if i != user:
                result[user][i] = 0 
    
    for trans in group["transactions"].values():
        for b in trans["breakdown"]:
            if b != trans["paidBy"]:
                result[b][trans["paidBy"]] += float(Fraction(trans["breakdown"][b])) * float(trans["amount"])

    for p in result:
        for o in result[p]:
            if result[p][o] >= result[o][p]:
                tmp = result[p][o]
                result[p][o] -= result[o][p]
                result[o][p] -= tmp 

    for user1 in result:
        for user2 in result[user1]:
            result[user1][user2] = round(result[user1][user2],2)

    return jsonify(result)

#will require the url to have the correct format where the groupID is passed in the url
#e.g http://127.0.0.1:5000/get_stats?groupID=1
#returns a dict with each key being the type of transaction and the corresponding value being the amount spent
#e.g
#{
#   "Agricultural Services": 203,
#   "Contracted Services": 30,
#   "Transportation Services": 0,
#   "Utility Services": 700,
#   "Retail Outlet Services": 0,
#   "Clothing Stores": 0,
#   "Miscellaneous Stores": 41,
#   "Business Services": 90,
#   "Professional Services and Membership Organizations": 0,
#   "Government Services": 1030,
#   "Airlines": 0,
#   "Car Rental": 200,
#   "Lodging": 600,
#}
@app.route('/get_stats', methods=["GET"])
def get_stats():
    groupID = request.args.get("groupID")
    result = {
        "Agricultural Services": 0,
        "Contracted Services": 0,
        "Transportation Services": 0,
        "Utility Services": 0,
        "Retail Outlet Services": 0,
        "Clothing Stores": 0,
        "Miscellaneous Stores": 0,
        "Business Services": 0,
        "Professional Services and Membership Organizations": 0,
        "Government Services": 0,
        "Airlines": 0,
        "Car Rental": 0,
        "Lodging": 0,
    }
    group = groups.find_one({"groupID": str(groupID)})
    for trans in group["transactions"].values():
        code = int(trans["merchantCatergoryCode"])
        amount = float(trans["amount"])
        if 1 <= code <= 1499:
            result["Agricultural Services"] += amount
        elif 1500 <= code <= 2999:
            result["Contracted Services"] += amount
        elif 4000 <= code <= 4799:
            result["Transportation Services"] += amount
        elif 4800 <= code <= 4999:
            result["Utility Services"] += amount
        elif 5000 <= code <= 5599:
            result["Retail Outlet Services"] += amount
        elif 5600 <= code <= 5699:
            result["Clothing Stores"] += amount
        elif 5700 <= code <= 7299:
            result["Miscellaneous Stores"] += amount
        elif 7300 <= code <= 7999:
            result["Business Services"] += amount
        elif 8000 <= code <= 8999:
            result["Professional Services and Membership Organizations"] += amount
        elif 9000 <= code <= 9999:
            result["Government Services"] += amount
        elif 3000 <= code <= 3299:
            result["Airlines"] += amount
        elif 3300 <= code <= 3499:
            result["Car Rental"] += amount
        elif 3500 <= code <= 3999:
            result["Lodging"] += amount
    '''
    0001–1499 Agricultural Services
    1500–2999 Contracted Services
    4000–4799 Transportation Services
    4800–4999 Utility Services
    5000–5599 Retail Outlet Services
    5600–5699 Clothing Stores
    5700–7299 Miscellaneous Stores
    7300–7999 Business Services
    8000–8999 Professional Services and Membership Organizations
    9000–9999 Government Services
    3000–3299 Airlines
    3300–3499 Car Rental
    3500–3999 Lodging
    '''
    return jsonify(result)

if __name__ == '__main__':
    app.run()
