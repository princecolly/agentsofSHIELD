from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'gh0strid3r'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute(query)

        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            if username == 'phil':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('profile'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        
        return render_template('profile.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'username' in session and session['username'] == 'phil':
        return render_template('admin.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])  # type: ignore
def upload_file():
    if 'username' in session and session['username'] == 'phil':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file.save(os.path.join(app.config['missions'], file.filename)) # type: ignore
            return redirect(url_for('admin'))
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)