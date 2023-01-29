from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to the database
conn = sqlite3.connect('phone_directory.db', check_same_thread=False)
cursor = conn.cursor()

# Create the phone directory table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS phone_directory (id INTEGER PRIMARY KEY, name TEXT, phone_number TEXT)''')
conn.commit()

# Homepage (index template)
@app.route('/')
def index():
    # Get all entries from the phone directory
    cursor.execute('SELECT * FROM phone_directory')
    entries = cursor.fetchall()
    return render_template('index.html', entries=entries)

# Add new entry
@app.route('/add', methods=['POST'])
def add_entry():
    # Get the name and phone number from the form
    name = request.form['name']
    phone_number = request.form['phone']

    # Insert the new entry into the phone directory
    cursor.execute('INSERT INTO phone_directory (name, phone_number) VALUES (?, ?)', (name, phone_number))
    conn.commit()
    return redirect(url_for('index'))

# View an entry
@app.route('/view/<int:id>')
def view_entry(id):
    # Get the specified entry from the phone directory
    cursor.execute('SELECT * FROM phone_directory WHERE id=?', (id,))
    entry = cursor.fetchone()
    return render_template('view.html', entry=entry)

# Update an entry
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_entry(id):
    if request.method == 'GET':
        # Get the specified entry from the phone directory
        cursor.execute('SELECT * FROM phone_directory WHERE id=?', (id,))
        entry = cursor.fetchone()
        return render_template('update.html', entry=entry)
    else:
        # Get the updated name and phone number from the form
        name = request.form['name']
        phone_number = request.form['phone']

        # Update the entry in the phone directory
        cursor.execute('UPDATE phone_directory SET name=?, phone_number=? WHERE id=?', (name, phone_number, id))
        conn.commit()
        return redirect(url_for('index'))

# Delete an entry
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_entry(id):
    # Delete the specified entry from the phone directory
    cursor.execute('DELETE FROM phone_directory WHERE id=?', (id,))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
