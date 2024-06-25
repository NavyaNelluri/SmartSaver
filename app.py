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
                return redirect(url_for('home'))

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
                return redirect(url_for('dashboard'))

            else:
                flash('Invalid username or password', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

        finally:
            cursor.close()

    return render_template('home.html')



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('home'))

    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        username = session['username']
        form_type = request.form['form_type']
        frequency = request.form['frequency']
        notes = request.form['Notes']
        amount = float(request.form['dollars'])

        try:
            if form_type == 'expense':
                expense_type = request.form['expense_type']
                cursor.execute("""
                    INSERT INTO expense_tracker (username, frequency, expense_type, notes, amount)
                    VALUES (%s, %s, %s, %s, %s)
                """, (username, frequency, expense_type, notes, amount))
                conn.commit()
                flash('Expense added successfully', 'success')

            elif form_type == 'income':
                income_source = request.form['Notes']  # Adjust based on your form
                cursor.execute("""
                    INSERT INTO income_tracker (username, frequency, amount, income_source)
                    VALUES (%s, %s, %s, %s)
                """, (username, frequency, amount, income_source))
                conn.commit()
                flash('Income added successfully', 'success')

        except Exception as e:
            flash(f'Error adding entry: {str(e)}', 'error')

    try:
        # Fetch expenses for the current user
        cursor.execute("SELECT expense_type, SUM(amount) AS TotalSpent FROM expense_tracker WHERE username = %s GROUP BY expense_type", (session['username'],))
        expenses = cursor.fetchall()
        expense_labels = []
        expense_data = []
        for expense in expenses:
            expense_labels.append(expense[0])
            expense_data.append(float(expense[1]))

        # Fetch income for the current user
        cursor.execute("SELECT income_source, SUM(amount) AS TotalEarned FROM income_tracker WHERE username = %s GROUP BY income_source", (session['username'],))
        incomes = cursor.fetchall()
        income_labels = []
        income_data = []
        for income in incomes:
            income_labels.append(income[0])
            income_data.append(float(income[1]))

    except Exception as e:
        flash(f'Error fetching data: {str(e)}', 'error')
        expense_labels = []
        expense_data = []
        income_labels = []
        income_data = []

    finally:
        cursor.close()

    return render_template('dashboard.html', username=session['username'], expense_labels=expense_labels, expense_data=expense_data, income_labels=income_labels, income_data=income_data)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
