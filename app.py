from flask import Flask, request, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('welcome.html')

def init_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    # Create 'users' table
    try:
        c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    );
    ''')
        conn.commit()
    except sqlite3.OperationalError as e:
        print("Table couldn't be created:", e)
    conn.close()

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()

        return redirect(url_for('get_users'))
    return render_template('add_user.html')

@app.route('/get_users')
def get_users():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return str(users)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


