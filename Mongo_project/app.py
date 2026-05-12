from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://admin:admin123@cluster0.bqxv4v7.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["studentdb"]
collection = db["students"]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():

    try:
        name = request.form['name']
        email = request.form['email']

        data = {
            "name": name,
            "email": email
        }

        collection.insert_one(data)

        return redirect(url_for('success'))

    except Exception as e:
        return render_template('index.html', error=str(e))


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
