from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['flask_mongo_books']  # Database name

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validate user credentials from MongoDB
        user = db.akun.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        # Fetch book data from MongoDB
        books = db.books.find()
        return render_template('dashboard.html', books=books)
    else:
        return redirect(url_for('login'))

@app.route('/book/<book_id>')
def book_detail(book_id):
    if 'username' in session:
        # Fetch book details from MongoDB
        book = db.books.find_one({'_id': ObjectId(book_id)})
        return render_template('book_detail.html', book=book)
    else:
        return redirect(url_for('login'))

# Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True,port=5001)
if __name__ == '__main__':
    # Jalankan aplikasi menggunakan Waitress
    from waitress import serve
    serve(app, host='0.0.0.0', port=5001)