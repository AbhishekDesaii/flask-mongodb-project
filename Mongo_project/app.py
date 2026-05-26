from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://admin:admin123@cluster0.bqxv4v7.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)

# Existing Collection
db = client["studentdb"]
student_collection = db["students"]

# New Collection for To-Do Items
todo_collection = db["todoitems"]


@app.route('/')
def home():
    return render_template('index.html')


# Existing Student Form Route
@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']

        data = {
            "name": name,
            "email": email
        }

        student_collection.insert_one(data)

        return redirect(url_for('success'))

    except Exception as e:
        return render_template('index.html', error=str(e))


@app.route('/success')
def success():
    return render_template('success.html')


# ===============================
# New To-Do Page
# ===============================
@app.route('/todo')
def todo():
    return render_template('todo.html')


# ===============================
# New Backend API
# ===============================
@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    try:
        item_name = request.form.get('itemName')
        item_description = request.form.get('itemDescription')

        todo_data = {
            "itemName": item_name,
            "itemDescription": item_description
        }

        todo_collection.insert_one(todo_data)

        return jsonify({
            "message": "Todo item stored successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
