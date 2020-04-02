from flask import Flask, render_template, url_for, redirect, request
import ast
app = Flask(__name__)

#Hardcoded list for the personal transaction page
p_transactions = [
    {
        'name': 'Rent',
        'paidby': 'John',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 1040,
        'ratio': 0.25,
        'num': 3
    },
    {
        'name': 'Electricity Bill',
        'paidby': 'Bianca',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 294.79,
        'ratio': 0.25,
        'num': 3
    },
    {
        'name': 'Groceries',
        'paidby': 'You',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 103.80,
        'ratio': 0.25,
        'num': 3
    },
    {
        'name': 'Water Bill',
        'paidby': 'Michael',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 306.40,
        'ratio': 0.25,
        'num': 3
    }
]

#Hardcoded list for the shared transaction page
s_transactions = [
    {
        'name': 'Rent',
        'paidby': 'Bianca',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 1040,
        'ratio': 0.25,
        'num': 3
    },
    {
        'name': 'Electricity Bill',
        'paidby': 'Bianca',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 294.79,
        'ratio': 0.25,
        'num': 3
    },
    {
        'name': 'Groceries',
        'paidby': 'You',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 103.80,
        'ratio': 0.25,
        'num': 3
    },
    {
        'name': 'Water Bill',
        'paidby': 'Michael',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 306.40,
        'ratio': 0.25,
        'num': 3
    },
    {
        'name': 'Gas Bill',
        'paidby': 'You',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 420.69,
        'ratio': 0.25,
        'num': 3
    },
    {
        'name': 'Rent',
        'paidby': 'Bianca',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 1040,
        'ratio': 0.25,
        'num': 3
    },
    {
        'name': 'Electricity Bill',
        'paidby': 'Bianca',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 294.79,
        'ratio': 0.25,
        'num': 3
    },
    {
        'name': 'Groceries',
        'paidby': 'You',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 103.80,
        'ratio': 0.25,
        'num': 3
    }
]

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/analytics')
def analytics():
    return render_template("Analytics.html")

#takes in a transaction to display
#transaction is passed as a string and needs to be converted to a dict
@app.route("/breakdown/<trans>", methods=['GET', 'POST'])
def breakdown(trans):
    trans = ast.literal_eval(trans)
    return render_template("breakdown.html", trans=trans)

#is the function to display a list of all personal transaction in p_transactions
#takes in a transaction to be removed from personal transactions and added to shared transactions when the '+' button is clicked on the transaction
#the argument passed may be 'ignore' which is used when accessing the page from dashboard or breadcrumb and will not change the p_transaction or s_transaction lists
#This page also handles adding transaction which will pick up any POST requests and create a new transaction and append it to p_transaction
@app.route("/personal_transactions/<rem_trans>", methods=['GET', 'POST'])
def personal_transactions(rem_trans):
    if rem_trans != 'ignore':
        rem_trans = ast.literal_eval(rem_trans)
        s_transactions.append(rem_trans)
        p_transactions.remove(rem_trans)

    if request.method == 'POST':
        data = request.form
        new_trans = {
            'name': data['name'],
            'paidby': 'You',
            'members': ['John', 'Bianca', 'Michael'],
            'price': float(data['cost']),
            'ratio': 0.25,
            'num': 3
        }
        p_transactions.append(new_trans)            
    return render_template("PersonalTransactions.html", transactions=p_transactions)

#takes in a transaction to display
#transaction is passed as a string and needs to be converted to a dict
@app.route("/review/<trans>")
def review(trans):
    trans = ast.literal_eval(trans)
    return render_template("review.html", trans=trans)

@app.route("/shared_transactions")
def shared_transactions():
    return render_template("Shared_Transaction_Hist.html", transactions=s_transactions)

if __name__ == '__main__':
    app.run(debug=True)