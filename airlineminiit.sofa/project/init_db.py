import sqlite3
import os

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'flights.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS airports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            airport_code TEXT,
            airport_name TEXT,
            state TEXT
        )
    ''')
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
    print("Database initialized successfully.")

def populate_airports():
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    airports_data = [
        ('AOR', 'Sultan Abdul Halim Airport', 'Alor Setar'),
        ('BTU', 'Bintulu Airport', 'Bintulu'),
        ('JHB', 'Senai International Airport', 'Johor Bahru'),
        ('KBR', 'Sultan Ismail Petra Airport', 'Kota Bharu'),
        ('BKI', 'Kota Kinabalu International Airport', 'Kota Kinabalu'),
        ('KUL', 'Kuala Lumpur International Airport', 'Kuala Lumpur'),
        ('TGG', 'Sultan Mahmud Airport', 'Kuala Terengganu'),
        ('KUA', 'Kuantan Airport', 'Kuantan'),

    ]
    c.executemany('INSERT INTO airports (airport_code, airport_name, state) VALUES (?, ?, ?)', airports_data)
    conn.commit()
    conn.close()
    print("Airports table populated successfully.")

if __name__ == '__main__':
    init_db()
    populate_airports()
