from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database URIs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # User-related data
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models

# User model to store user information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Selection model to store baggage, assistance, meal selection, etc.
class Selection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    baggage_weight = db.Column(db.Integer, nullable=False)
    special_assistance = db.Column(db.Integer, nullable=False)
    meal_option = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', backref=db.backref('selections', lazy=True))

    def __repr__(self):
        return f"Selection('{self.user_id}', '{self.baggage_weight}', '{self.special_assistance}', '{self.meal_option}')"

# Route to display all users


@app.route('/')
def base():
    users = User.query.all()  # Get all users from the 'users' table
    return render_template('base.html', users=users)

@app.route('/baggage')
def baggage():
    return render_template('baggage.html')

@app.route('/meal')
def meal():
    return render_template('meal.html')

@app.route('/assistance')
def assistance():
    return render_template('assistance.html')

@app.route('/seats')
def seats():
    return render_template('seats.html')

# Route to handle user selection form submission (for baggage, assistance, meal, etc.)
@app.route('/select/<int:user_id>', methods=['GET', 'POST'])
def select(user_id):
    user = User.query.get_or_404(user_id)  # Fetch the user by ID
    
    if request.method == 'POST':
        baggage_weight = request.form.get('baggage_weight')
        special_assistance = request.form.get('special_assistance')
        meal_option = request.form.get('meal_option')
        
        # Save the selection in the database
        selection = Selection(
            user_id=user.id,
            baggage_weight=baggage_weight,
            special_assistance=special_assistance,
            meal_option=meal_option
        )
        db.session.add(selection)
        db.session.commit()
        
        return redirect(url_for('base'))  # Redirect back to the user listing

    return render_template('select.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
