from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'b1727199ba249aec98e0b807'
db = SQLAlchemy(app)
from market import routes

if __name__=="__main__":
    app.run(debug=True)