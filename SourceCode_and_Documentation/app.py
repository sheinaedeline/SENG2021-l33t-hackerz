from flask import Flask, render_template, url_for, redirect, request
import ast
app = Flask(__name__)

transactions = [
    {
        'name': 'Movies',
        'paidby': 'John',
        'members': ['John', 'Bianca'],
        'price': 28.50,
        'ratio': 0.333,
        'num': 2
    },
    {
        'name': 'Dinner',
        'paidby': 'Bianca',
        'members': ['Bianca'],
        'price': 79.40,
        'ratio': 0.5,
        'num': 1
    },
    {
        'name': 'Groceries',
        'paidby': 'John',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 103.80,
        'ratio': 0.25,
        'num': 3
    },
    {
        'name': 'Gaming',
        'paidby': 'Michael',
        'members': ['Michael'],
        'price': 59.95,
        'ratio': 0.5,
        'num': 1
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

@app.route("/breakdown/<trans>", methods=['GET', 'POST'])
def breakdown(trans):
    trans = ast.literal_eval(trans)
    return render_template("breakdown.html", trans=trans)

@app.route("/personal_transactions", methods=['GET', 'POST'])
def personal_transactions():
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
        transactions.append(new_trans)

    return render_template("PersonalTransactions.html", transactions=transactions)

@app.route("/review/<trans>")
def review(trans):
    trans = ast.literal_eval(trans)
    return render_template("review.html", trans=trans)

@app.route("/shared_transactions")
def shared_transactions():
    return render_template("Shared_Transaction_Hist.html")

if __name__ == '__main__':
    app.run(debug=True)