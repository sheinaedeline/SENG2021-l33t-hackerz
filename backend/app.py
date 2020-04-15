from flask import Flask
import pymongo
import json
app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0-o08tg.mongodb.net/test?retryWrites=true&w=majority")
database = myclient["MicaDatabase"]
groups = database["Groups"]

with open("../bankingAPI/getbanktransactions.json") as json_file:
    API_data = json.load(json_file)

@app.route('/')
def hello():
    return "Hello World!"

#may need change
def login(username, password):
    if username is "username" and password is "password":
        return True
    else:
        return False

#done
def get_shared_trans(group_ID):
    result = []
    group = groups.find_one({"groupID": str(group_ID)})
    for trans in group["transactions"].values():
        result.append(trans)
    return result

#done
def put_trans(transaction, group_ID):
    field = "transactions." + str(transaction["transactionID"])
    return groups.update({"groupID": str(group_ID)}, {'$set': {field: transaction}})["updatedExisting"]

#done
def upd_trans(new_trans, old_trans_ID, group_ID):
    field = "transactions." + str(old_trans_ID)
    return groups.update({"groupID": str(group_ID)}, {'$set': {field: new_trans}})["updatedExisting"]

#done
def put_rule(rule, group_ID):
    return groups.update({"groupID": str(group_ID)}, {'$push': {"rules": rule}})["updatedExisting"]

#done
def get_rules(group_ID):
    return groups.find_one({"groupID": str(group_ID)})["rules"]

#TODO
def get_total(group_ID):
    return

#TODO
def get_stats(group_ID):
    return

if __name__ == '__main__':
    app.run()
