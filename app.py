from flask import Flask, render_template, request, redirect, url_for, session, flash
import snowflake.connector as snowflake

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Snowflake database connection parameters
snowflake_account = 'ywonoeq-up08793'
snowflake_user = 'SMARTSAVER'  
snowflake_password = 'SmartSaver_pswd1'  
snowflake_database = 'SMARTSAVER'  
snowflake_schema = 'SCH_SMARTSAVER'
snowflake_warehouse = 'COMPUTE_WH'


# Function to establish Snowflake database connection
def get_db():
    conn = snowflake.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )
    return conn



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        try:
            # Check if user already exists
            cursor.execute("SELECT * FROM USERS WHERE UserName = %s", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash('Username already exists. Please choose another one.', 'error')
            else:
                # Insert new user
                cursor.execute("INSERT INTO USERS (FirstName, LastName, UserName, Password, Email) "
                               "VALUES (%s, %s, %s, %s, %s)",
                               (firstname, lastname, username, password, email))
                conn.commit()
                flash('Registration successful', 'success')
                return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

        finally:
            cursor.close()

    return render_template('register.html')
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()

        username = request.form['username']
        password = request.form['password']

        try:
            # Validate user credentials
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                           (username, password))
            user = cursor.fetchone()
            if user:
                session['username'] = username
                flash('Login successful', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

        finally:
            cursor.close()

    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
