from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
app = Flask(__name__)
ENV='Prod'
if ENV == 'Dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:manish@1234@localhost/Feedback'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cxpfmqqejxfasr:3b877f163532d1f39dcfcac248e1857c9719f7dd68a4f9f5d22647ab42d69a13@ec2-52-45-73-150.compute-1.amazonaws.com:5432/db5i0ajvoc38q2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=False)
    dealer = db.Column(db.String(200), unique=False)
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())
    def __init__(self,customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

@app.route('/')

def index():
    return render_template('index.html')
@app.route('/submit', methods = ['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['Comments']
        #print(customer, dealer, rating, comments)
        if customer == '' or  dealer == '':
            return render_template('index.html', message='Please fill required field ')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('Sucess.html')

if __name__ == "__main__":
    app.run()
