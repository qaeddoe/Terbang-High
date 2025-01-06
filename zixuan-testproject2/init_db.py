import sqlite3

conn = sqlite3.connect('./instance/preference.db')
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE pref (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    departure_baggage INTEGER NOT NULL,
                    return_baggage INTEGER NOT NULL,
                    departure_meals TEXT NOT NULL,
                    return_meals TEXT NOT NULL,
                    departure_assistance VARCHAR(100) NOT NULL,
                    return_assistance VARCHAR(100) NOT NULL,
                    departure_seat TEXT,
                    return_seat TEXT
               );
               ''')

conn.commit()
conn.close()

print("Database initialized and saved as 'preference.db' in the 'instance' folder.")
