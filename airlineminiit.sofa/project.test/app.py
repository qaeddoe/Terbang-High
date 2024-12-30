from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    from_city = request.form.get('from')
    to_city = request.form.get('to')
    depart_date = request.form.get('depart')
    return_date = request.form.get('return', None)
    passengers = request.form.get('passengers')
    cabin_class = request.form.get('cabin_class')
    
    return f"From: {from_city}, To: {to_city}, Depart: {depart_date}, Return: {return_date}, Passengers: {passengers}, Cabin Class: {cabin_class}"

if __name__ == '__main__':
    app.run(debug=True)
