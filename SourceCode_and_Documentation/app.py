from flask import Flask, render_template, url_for, redirect
import ast
app = Flask(__name__)

transactions = [
    {
        'name': 'Movies',
        'paidby': 'John',
        'members': ['John', 'Bianca'],
        'price': 28.50,
        'ratio': 0.333
    },
    {
        'name': 'Dinner',
        'paidby': 'Bianca',
        'members': ['Bianca'],
        'price': 79.40,
        'ratio': 0.5
    },
    {
        'name': 'Groceries',
        'paidby': 'John',
        'members': ['John', 'Bianca', 'Michael'],
        'price': 103.80,
        'ratio': 0.25
    },
    {
        'name': 'Gaming',
        'paidby': 'Michael',
        'members': ['Michael'],
        'price': 59.95,
        'ratio': 0.5
    }
]

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/analytics')
def analytics():
    return render_template("Analytics.html")

@app.route("/breakdown/<trans>", methods=['GET', 'POST'])
def breakdown(trans):
    trans = ast.literal_eval(trans)
    return render_template("breakdown.html", trans=trans)

@app.route("/personal_transactions")
def personal_transactions():
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