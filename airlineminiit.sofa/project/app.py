from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

import sqlite3

def populate_airports():
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    
    airports_data = [
        ('JFK', 'John F. Kennedy International Airport', 'New York'),
        ('LAX', 'Los Angeles International Airport', 'California'),
        ('HRE', 'O\'Hare International Airport', 'Illinois'),
        ('DAL', 'Dallas/Fort Worth International Airport', 'Texas')
    ]
    
    c.executemany('INSERT INTO airports (airport_code, airport_name, state) VALUES (?, ?, ?)', airports_data)
    conn.commit()
    conn.close()
    print("Airports table populated successfully.")



def init_db():
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    try:
        c.execute('''
            CREATE TABLE IF NOT EXISTS airports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                airport_code TEXT,
                airport_name TEXT,
                state TEXT
            )
        ''')
        print("Airports table created successfully.")
        # Create other tables...
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()




@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()

    # Query all airports with additional details
    c.execute('SELECT airport_code, airport_name, state FROM airports')
    airports = c.fetchall()  # Fetch all results from the airports table

    conn.close()

    flights = []
    departure_city = destination_city = trip_type = departure_date = None

    if request.method == 'POST':
        departure_city = request.form['departure_city']
        destination_city = request.form['destination_city']
        trip_type = request.form['trip_type']
        departure_date = request.form['departure_date']

        conn = sqlite3.connect('flights.db')
        c = conn.cursor()

        c.execute('''SELECT * FROM flights WHERE departure_city = ? AND destination_city = ?''', (departure_city, destination_city))

        flights = c.fetchall()
        conn.close()

    return render_template('index.html', 
                           flights=flights, 
                           departure_city=departure_city,
                           destination_city=destination_city, 
                           trip_type=trip_type, 
                           departure_date=departure_date,
                           airports=airports)




@app.route('/book', methods=['POST'])
def book():
    departure_city = request.form['departure_city']
    destination_city = request.form['destination_city']
    departure_date = request.form['departure_date']
    return_date = request.form.get('return_date')  # Optional for one-way trips
    trip_type = request.form['trip_type']

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
    with app.app_context():
        init_db()
    app.run(debug=True)
