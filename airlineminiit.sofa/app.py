from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    departure_city TEXT NOT NULL,
                    destination_city TEXT NOT NULL,
                    flight_type TEXT NOT NULL,
                    flight_class TEXT NOT NULL,
                    departure_time TEXT NOT NULL,
                    arrival_time TEXT NOT NULL,
                    fare INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

# Home route - Display booking form
@app.route('/')
def home():
    return render_template('index.html')

# Route for submitting the booking
@app.route('/book', methods=['POST'])
def book():
    departure_city = request.form['departure_city']
    destination_city = request.form['destination_city']
    flight_type = request.form['flight_type']
    flight_class = request.form['flight_class']
    departure_time = request.form['departure_time']
    arrival_time = request.form['arrival_time']
    fare = request.form['fare']

    # Store in the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''INSERT INTO bookings (departure_city, destination_city, flight_type, flight_class, 
                                       departure_time, arrival_time, fare) VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (departure_city, destination_city, flight_type, flight_class, departure_time, arrival_time, fare))
    conn.commit()
    conn.close()

    return redirect('/flights')

# Route for viewing available flights
@app.route('/flights')
def flights():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    flights = c.fetchall()
    conn.close()
    return render_template('flights.html', flights=flights)

# Route for the Flight Selection page
@app.route('/select-flight', methods=['GET'])
def select_flight():
    # Example flight data with base prices for Economy
    base_flights = [
        {"id": 1, "airline": "AirAsia", "flight_number": "AK2169", "departure_time": "6:10 AM", "arrival_time": "7:25 AM", "duration": "1h 15m", "base_price": 150},
        {"id": 2, "airline": "Malaysia Airlines", "flight_number": "MH1201", "departure_time": "8:40 AM", "arrival_time": "9:55 AM", "duration": "1h 15m", "base_price": 170},
        {"id": 3, "airline": "Firefly", "flight_number": "FY2190", "departure_time": "10:10 AM", "arrival_time": "11:25 AM", "duration": "1h 15m", "base_price": 160},
        {"id": 4, "airline": "AirAsia", "flight_number": "AK2173", "departure_time": "12:30 PM", "arrival_time": "1:45 PM", "duration": "1h 15m", "base_price": 200},
        {"id": 5, "airline": "Malaysia Airlines", "flight_number": "MH1203", "departure_time": "2:00 PM", "arrival_time": "3:15 PM", "duration": "1h 15m", "base_price": 190},
        {"id": 6, "airline": "Firefly", "flight_number": "FY2192", "departure_time": "4:20 PM", "arrival_time": "5:35 PM", "duration": "1h 15m", "base_price": 210},
        {"id": 7, "airline": "AirAsia", "flight_number": "AK2181", "departure_time": "6:40 PM", "arrival_time": "7:55 PM", "duration": "1h 15m", "base_price": 180},
        {"id": 8, "airline": "Malaysia Airlines", "flight_number": "MH1207", "departure_time": "9:00 PM", "arrival_time": "10:15 PM", "duration": "1h 15m", "base_price": 220},
    ]

    # Cabin class price multipliers
    cabin_multipliers = {
        "Economy": 1.0,
        "Premium Economy": 1.5,
        "Business": 2.0,
        "First Class": 3.0
    }

    # Retrieve selected cabin class from the booking form
    selected_cabin_class = request.args.get('cabin_class', 'Economy')
    multiplier = cabin_multipliers.get(selected_cabin_class, 1.0)

    # Adjust prices based on the selected cabin class
    flights = [
        {
            **flight,
            "price": round(flight["base_price"] * multiplier)  # Calculate adjusted price
        }
        for flight in base_flights
    ]

    # Retrieve other search criteria
    search_criteria = {
        "departure_city": request.args.get('departure_city', 'Unknown'),
        "destination_city": request.args.get('destination_city', 'Unknown'),
        "departure_date": request.args.get('departure_date', 'Unknown'),
        "arrival_date": request.args.get('arrival_date', None),
        "passengers": request.args.get('passengers', '1'),
        "cabin_class": selected_cabin_class
    }

    return render_template('select_flight.html', flights=flights, **search_criteria)


#PAGE3
@app.route('/select-returning-flight', methods=['GET'])
def select_returning_flight():
    # Debugging logs
    print("Query Parameters:", request.args)
    # Retrieve data from the previous page
    departure_city = request.args.get('departure_city')
    destination_city = request.args.get('destination_city')
    departure_date = request.args.get('departure_date')
    arrival_date = request.args.get('arrival_date')
    cabin_class = request.args.get('cabin_class')
    passengers = request.args.get('passengers')

    # Define returning flight options
    returning_flights = [
        {"id": 1, "airline": "AirAsia", "flight_number": "AK2243", "departure_time": "6:10 AM", "arrival_time": "7:25 AM", "duration": "1h 15m", "base_price": 150},
        {"id": 2, "airline": "Malaysia Airlines", "flight_number": "MH1234", "departure_time": "8:40 AM", "arrival_time": "9:55 AM", "duration": "1h 15m", "base_price": 170},
        {"id": 3, "airline": "Firefly", "flight_number": "FY2176", "departure_time": "10:10 AM", "arrival_time": "11:25 AM", "duration": "1h 15m", "base_price": 160},
        {"id": 4, "airline": "AirAsia", "flight_number": "AK2190", "departure_time": "12:30 PM", "arrival_time": "1:45 PM", "duration": "1h 15m", "base_price": 200},
        {"id": 5, "airline": "Malaysia Airlines", "flight_number": "MH1234", "departure_time": "2:00 PM", "arrival_time": "3:15 PM", "duration": "1h 15m", "base_price": 190},
        {"id": 6, "airline": "Firefly", "flight_number": "FY2121", "departure_time": "4:20 PM", "arrival_time": "5:35 PM", "duration": "1h 15m", "base_price": 210},
        {"id": 7, "airline": "AirAsia", "flight_number": "AK2191", "departure_time": "6:40 PM", "arrival_time": "7:55 PM", "duration": "1h 15m", "base_price": 180},
        {"id": 8, "airline": "Malaysia Airlines", "flight_number": "MH1201", "departure_time": "9:00 PM", "arrival_time": "10:15 PM", "duration": "1h 15m", "base_price": 220},
    ]
    

    # Cabin class price multipliers
    cabin_multipliers = {
        "Economy": 1.0,
        "Premium Economy": 1.5,
        "Business": 2.0,
        "First Class": 3.0
    }

    multiplier = cabin_multipliers.get(cabin_class, 1.0)

    # Adjust prices based on the cabin class
    flights = [
        {
            **flight,
            "price": round(flight["base_price"] * multiplier)
        }
        for flight in returning_flights
    ]

    # Render the returning flight selection page
    return render_template(
        'select_returning_flight.html',
        flights=flights,
        departure_city=departure_city,
        destination_city=destination_city,
        departure_date=departure_date,
        arrival_date=arrival_date,
        passengers=passengers,
        cabin_class=cabin_class
    )

# Ensure the app is started correctly
if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)