from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3

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

# # Selection model to store baggage, assistance, meal selection, etc.
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
def index():
    users = User.query.all()  # Get all users from the 'users' table
    return render_template('addon.html', users=users)

# Route to handle dynamic content for the overlays
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
    
    print("hi")
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
        
        return redirect(url_for('addon'))  # Redirect back to the user listing

    return render_template('select.html', user=user)


@app.route('/submit/preference', methods=['POST'])
def submit_preference():
    conn = sqlite3.connect('./instance/preference.db', isolation_level=None)
    conn.execute('PRAGMA busy_timeout = 3000')
    conn.row_factory = sqlite3.Row

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid data format, expected a JSON object"}), 400

    type_of_data = data.get('type')
    user_id = data.get('userId')

    if not type_of_data or type_of_data not in ['meal', 'baggage', 'assistance', 'seat']:
        return jsonify({"status": "error", "message": "Invalid data type"}), 400

    departure_assistance = "None"
    return_assistance = "None"
    departure_baggage = "None"
    return_baggage = "None"
    departure_meals = "None"
    return_meals = "None"
    departure_seat = "None"
    return_seat = "None"

    try:
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute('SELECT * FROM pref WHERE user_id = ?', (user_id,))
        existing_user = cursor.fetchone()

        # If the user doesn't exist, insert a new record
        if not existing_user:
            cursor.execute('''
                INSERT INTO pref (user_id, departure_assistance, return_assistance, 
                                  departure_baggage, return_baggage, departure_meals, return_meals)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, departure_assistance, return_assistance, departure_baggage, return_baggage, departure_meals, return_meals))

        # Start a transaction
        cursor.execute('BEGIN TRANSACTION;')

        if type_of_data == 'baggage':
            baggage_data = data.get('data', [])
            if len(baggage_data) != 2:
                return jsonify({"status": "error", "message": "Invalid baggage data"}), 400

            departure_baggage = baggage_data[0]
            return_baggage = baggage_data[1]

            cursor.execute('''
                UPDATE pref
                SET departure_baggage = ?, return_baggage = ?
                WHERE user_id = ?
            ''', (departure_baggage, return_baggage, user_id))

        elif type_of_data == 'meal':
            meal_data = data.get('data', [])
            if len(meal_data) != 2:
                return jsonify({"status": "error", "message": "Invalid meal data"}), 400

            departure_meals = meal_data[0]
            return_meals = meal_data[1]

            cursor.execute('''
                UPDATE pref
                SET departure_meals = ?, return_meals = ?
                WHERE user_id = ?
            ''', (departure_meals, return_meals, user_id))

        elif type_of_data == 'assistance':
            assistance_data = data.get('data', [])
            if len(assistance_data) != 2:
                return jsonify({"status": "error", "message": "Invalid assistance data"}), 400

            departure_assistance = assistance_data[0]
            return_assistance = assistance_data[1]

            cursor.execute('''
                UPDATE pref
                SET departure_assistance = ?, return_assistance = ?
                WHERE user_id = ?
            ''', (departure_assistance, return_assistance, user_id))

        elif type_of_data == 'seat':
            seat_data = data.get('data', [])
            if len(seat_data) != 2:
                return jsonify({"status": "error", "message": "Invalid seat data"}), 400

            departure_seat = seat_data[0]
            return_seat = seat_data[1]

            cursor.execute('''
                UPDATE pref
                SET departure_seat = ?, return_seat = ?
                WHERE user_id = ?
            ''', (departure_seat, return_seat, user_id))

        # Commit the transaction
        conn.commit()

        return jsonify({"status": "success", "message": "Data updated successfully"}), 200

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()


@app.route('/get_preferences/<int:user_id>', methods=['GET'])
def get_preferences(user_id):
    conn = sqlite3.connect('./instance/preference.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            departure_baggage, return_baggage,
            departure_meals, return_meals,
            departure_assistance, return_assistance,
            departure_seat, return_seat
        FROM pref WHERE user_id = ?
    ''', (user_id,))
    preferences = cursor.fetchone()

    if preferences:
        # Collect all preferences
        all_preferences = {
            'departure_baggage': preferences['departure_baggage'],
            'return_baggage': preferences['return_baggage'],
            'departure_meals': preferences['departure_meals'],
            'return_meals': preferences['return_meals'],
            'departure_assistance': preferences['departure_assistance'],
            'return_assistance': preferences['return_assistance'],
            'departure_seat': preferences['departure_seat'],
            'return_seat': preferences['return_seat']
        }

        return jsonify(all_preferences)
    else:
        return jsonify({
            'departure_baggage': 'none',
            'return_baggage': 'none',
            'departure_meals': 'none',
            'return_meals': 'none',
            'departure_assistance': 'none',
            'return_assistance': 'none',
            'departure_seat': 'none',
            'return_seat': 'none'
        })


@app.route('/get_chosen_seats', methods=['GET'])
def get_selected_seats():
    try:
        conn = sqlite3.connect('./instance/preference.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, departure_seat, return_seat 
            FROM pref 
            WHERE departure_seat IS NOT NULL AND return_seat IS NOT NULL
        ''')
        
        rows = cursor.fetchall()

        seats = [dict(row) for row in rows]

        return jsonify({"status": "success", "seats": seats}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
