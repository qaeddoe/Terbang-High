from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            departure_city TEXT,
            destination_city TEXT,
            departure_time TEXT,
            arrival_time TEXT,
            flight_duration TEXT,
            fare_class TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            departure_city TEXT,
            destination_city TEXT,
            departure_date TEXT,
            return_date TEXT,
            trip_type TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route for Home (Search flights)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        departure_city = request.form['departure_city']
        destination_city = request.form['destination_city']
        trip_type = request.form['trip_type']
        departure_date = request.form['departure_date']
        
        # Get available flights from the database
        conn = sqlite3.connect('flights.db')
        c = conn.cursor()
        c.execute('''
            SELECT * FROM flights
            WHERE departure_city = ? AND destination_city = ?
        ''', (departure_city, destination_city))
        flights = c.fetchall()
        conn.close()

        return render_template('index.html', flights=flights, departure_city=departure_city,
                               destination_city=destination_city, trip_type=trip_type, 
                               departure_date=departure_date)
    return render_template('index.html')

# Route to handle booking a flight
@app.route('/book', methods=['POST'])
def book():
    departure_city = request.form['departure_city']
    destination_city = request.form['destination_city']
    departure_date = request.form['departure_date']
    return_date = request.form.get('return_date')
    trip_type = request.form['trip_type']

    # Store booking details in the database
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO bookings (departure_city, destination_city, departure_date, return_date, trip_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (departure_city, destination_city, departure_date, return_date, trip_type))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()  # Initialize the database when app starts
    app.run(debug=True)
