from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///selections.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Selection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    baggage_weight = db.Column(db.Integer, nullable=False)
    special_assistance = db.Column(db.Integer, nullable=False)
    meal_option = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Selection('{self.user_id}', '{self.baggage_weight}', '{self.wheelchair_option}', '{self.meal_option}')"

@app.route('/')
def index():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)
