from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import snowflake.connector as snowflake
import datetime
import timedelta
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your email provider's SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Replace with your email address
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  # Replace with your email address

mail = Mail(app)

# Snowflake database connection parameters
snowflake_account = 'zthubab-uq03646'
snowflake_user = 'SmartSaver'
snowflake_password = 'SmartSaverpswd01'
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

def send_email(subject, recipient, body):
    msg = Message(
        subject,
        sender=("SmartSaver", app.config['MAIL_USERNAME']),
        recipients=[recipient]
    )
    msg.body = body
    with app.app_context():
        mail.send(msg)

def send_expense_notification(user_email, user_name, expense_type, amount, frequency, notes):
    subject = "Expense Added Notification"
    body = f"""
    Hello {user_name},

    You have successfully added a new expense.

    Details:
    Expense Type: {expense_type}
    Amount: ${amount}
    Frequency: {frequency}
    Notes: {notes}

    Best regards,
    SmartSaver Team
    """
    send_email(subject, user_email, body)

def send_income_notification(user_email, user_name, income_source, amount, frequency):
    subject = "Income Added Notification"
    body = f"""
    Hello {user_name},

    You have successfully added a new income.

    Details:
    Income Source: {income_source}
    Amount: ${amount}
    Frequency: {frequency}

    Best regards,
    SmartSaver Team
    """
    send_email(subject, user_email, body)

def send_savings_goal_notification(user_email, user_name, goal_item, goal_amount, allocation_percentage, monthly_income):
    subject = "Savings Goal Added Notification"
    body = f"""
    Hello {user_name},

    You have successfully added a new savings goal.

    Details:
    Savings Goal Item: {goal_item}
    Savings Goal Amount: ${goal_amount}
    Allocation Percentage: {allocation_percentage}%
    Monthly Disposable Income: ${monthly_income}

    Best regards,
    SmartSaver Team
    """
    send_email(subject, user_email, body)

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
                body = f'Hello {firstname},\n\nYou have successfully registered.\n\nBest regards,\nSmartSaver Team'
                send_email("Welcome to SmartSaver!", email, body)
                return redirect(url_for('home'))

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

        finally:
            cursor.close()

    return render_template('register.html')
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    user = session['username']
    conn = get_db()
    cursor = conn.cursor()

    # Default masked password
    masked_password = None

    try:
        # Fetch current user information
        cursor.execute("SELECT FirstName, LastName, UserName, Email, Password FROM USERS WHERE UserName = %s", (user,))
        user_data = cursor.fetchone()
        
        if request.method == 'POST':
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            username = request.form['username']
            email = request.form['email']
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            # Validate current password
            cursor.execute("SELECT Password FROM USERS WHERE UserName = %s", (user,))
            stored_password = cursor.fetchone()[0]

            if stored_password != current_password:
                flash('Current password is incorrect.', 'error')
            elif new_password != confirm_password:
                flash('New passwords do not match.', 'error')
            else:
                # Update user information
                cursor.execute("UPDATE USERS SET FirstName = %s, LastName = %s, UserName = %s, Email = %s, Password = %s WHERE UserName = %s and Password = %s",
                               (firstname, lastname, username, email, new_password, user, current_password))
                conn.commit()
                flash('Profile updated successfully!', 'success')
                
                # Update the current_user attributes to reflect changes
                user = username  # Update session username
                session['username'] = username

        # Mask the password (show only the last 3 characters)
        if user_data:
            masked_password = '***' + user_data[4][-3:]
        else:
            masked_password = '***'  # Default masked password if user data is not found

    except Exception as e:
        flash(f'Error updating profile: {str(e)}', 'error')

    finally:
        cursor.close()

    return render_template('settings.html', user=user_data, masked_password=masked_password)


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
            # Fetch user's first name and email
            cursor.execute("SELECT FirstName, Email FROM USERS WHERE UserName = %s", (username,))
            user_info = cursor.fetchone()
            first_name = user_info[0]
            email = user_info[1]

            if form_type == 'expense':
                expense_type = request.form['expense_type']
                cursor.execute("""
                    INSERT INTO expense_tracker (username, frequency, expense_type, notes, amount)
                    VALUES (%s, %s, %s, %s, %s)
                """, (username, frequency, expense_type, notes, amount))
                conn.commit()
                flash('Expense added successfully', 'success')
                send_expense_notification(email, first_name, expense_type, amount, frequency, notes)
            elif form_type == 'income':
                income_source = request.form['Notes']  # Adjust based on your form
                cursor.execute("""
                    INSERT INTO income_tracker (username, frequency, amount, income_source)
                    VALUES (%s, %s, %s, %s)
                """, (username, frequency, amount, income_source))
                conn.commit()
                flash('Income added successfully', 'success')
                send_income_notification(email, first_name, income_source, amount, frequency)
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

@app.route('/SavingsGoals', methods=['GET', 'POST'])
def savings_goals():
    if 'username' not in session:
        flash('Please log in to access the savings goals page.', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = session['username']
        SavingsGoalItem = request.form['SavingsGoalItem']
        SavingsGoalAmount = float(request.form['SavingsGoalAmount'])
        MonthlyDisposableIncome = request.form['MonthlyIncome']
        AllocationPercentage = request.form['AllocationPercentage']

        try:
            conn = get_db()
            cursor = conn.cursor()

            # Fetch user's first name
            cursor.execute("SELECT FirstName, Email FROM USERS WHERE UserName = %s", (username,))
            user_info = cursor.fetchone()
            first_name = user_info[0]
            email = user_info[1]

            cursor.execute("""
                INSERT INTO SAVINGS_GOAL_TRACKER (username, SavingsGoalItem, SavingsGoalAmount, AllocationPercentage, MonthlyDisposableIncome, created_at)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP())
            """, (username, SavingsGoalItem, SavingsGoalAmount, AllocationPercentage, MonthlyDisposableIncome))
            conn.commit()
            send_savings_goal_notification(email, first_name, SavingsGoalItem, SavingsGoalAmount, AllocationPercentage, MonthlyDisposableIncome)
            flash('Goal saved successfully and email notification sent', 'success')
            cursor.close()
        except Exception as e:
            flash(f'Error saving goal: {str(e)}', 'error')
        finally:
            conn.close()

    return render_template('SavingsGoals.html', username=session['username'])


@app.route('/ViewGoals', methods=['GET', 'POST'])
def view_goals():
    username = session['username']

    conn = get_db()
    cursor = conn.cursor()
    goals_with_months_left = []
    today = datetime.now()

    try:
        cursor.execute("SELECT username, SavingsGoalItem, SavingsGoalAmount, AllocationPercentage, MonthlyDisposableIncome, created_at FROM SAVINGS_GOAL_TRACKER WHERE username=%s", (username,))
        goals = cursor.fetchall()
        for goal in goals:
            created_at = goal[5]  # Assuming created_at is the 6th element in each goal tuple
            savings_goal_amount = float(goal[2])
            allocation_percentage = float(goal[3])
            monthly_income = float(goal[4])

            # Calculate monthly allocation amount
            monthly_allocation = monthly_income * (allocation_percentage / 100)

            # Calculate number of months required to reach the savings goal
            months_to_goal = savings_goal_amount / monthly_allocation

            # Calculate the target date to achieve the goal
            target_date = created_at + timedelta(days=months_to_goal * 30)

            # Calculate months left from today to the target date
            months_left = (target_date.year - today.year) * 12 + target_date.month - today.month
            if target_date.day < today.day:
                months_left -= 1

            goals_with_months_left.append((*goal, months_left))

        return render_template('ViewGoals.html', username=username, goals=goals_with_months_left)

    except Exception as e:
        # Handle error (print/log/display error message)
        print(f"Error fetching goals: {str(e)}")
        return render_template('ViewGoals.html', message="Error fetching goals. Please try again later.")

    finally:
        cursor.close()
        conn.close()

@app.route('/view_income')
def view_income():
    if 'username' not in session:
        flash('Please log in to view income.', 'error')
        return redirect(url_for('home'))

    conn = get_db()
    cursor = conn.cursor()

    try:
        username = session['username']
        cursor.execute("SELECT income_source, frequency, amount, id FROM income_tracker WHERE username = %s", (username,))
        incomes = cursor.fetchall()
    except Exception as e:
        flash(f'Error fetching income data: {str(e)}', 'error')
        incomes = []

    finally:
        cursor.close()

    return render_template('ViewIncome.html', incomes=incomes)

@app.route('/edit_income/<int:income_id>', methods=['GET', 'POST'])
def edit_income(income_id):
    if 'username' not in session:
        flash('Please log in to edit income.', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()

        try:
            frequency = request.form.get('frequency')
            notes = request.form.get('Notes')
            dollars = request.form.get('dollars')

            cursor.execute("UPDATE income_tracker SET frequency = %s, income_source = %s, amount = %s WHERE id = %s",
                           (frequency, notes, dollars, income_id))
            conn.commit()

            flash('Income updated successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error updating income: {str(e)}', 'error')
        finally:
            cursor.close()

    return redirect(url_for('view_income'))

@app.route('/view_expenses')
def view_expenses():
    if 'username' not in session:
        flash('Please log in to view expenses.', 'error')
        return redirect(url_for('home'))

    conn = get_db()
    cursor = conn.cursor()

    try:
        username = session['username']
        cursor.execute("SELECT expense_type, frequency, amount, notes, id FROM expense_tracker WHERE username = %s", (username,))
        expenses = cursor.fetchall()
    except Exception as e:
        flash(f'Error fetching expense data: {str(e)}', 'error')
        expenses = []
    finally:
        cursor.close()

    return render_template('ViewExpense.html', expenses=expenses)

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    if 'username' not in session:
        flash('Please log in to edit expenses.', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()

        try:
            frequency = request.form.get('frequency')
            notes = request.form.get('Notes')
            dollars = request.form.get('dollars')
            expense_type = request.form.get('expense_type')

            cursor.execute("UPDATE expense_tracker SET frequency = %s, notes = %s, amount = %s, expense_type = %s WHERE id = %s",
                           (frequency, notes, dollars, expense_type, expense_id))
            conn.commit()

            flash('Expense updated successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error updating expense: {str(e)}', 'error')
        finally:
            cursor.close()

    return redirect(url_for('view_expenses'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Validate passwords
        if new_password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('forgot_password.html')

        # Check if the username and email match in the database
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM USERS WHERE username = %s AND email = %s", (username, email))
            user = cursor.fetchone()

            if user:
                # Update the user's password
                cursor.execute("UPDATE USERS SET Password = %s WHERE username = %s AND email = %s", (new_password, username, email))
                conn.commit()
                flash('Password has been reset successfully.', 'success')
                return redirect(url_for('home'))
            else:
                flash('Username and email do not match.', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()

    return render_template('forgot_password.html')

@app.route('/delete_goal', methods=['POST'])
def delete_goal():
    if 'username' not in session:
        flash('Please log in to delete goals.', 'error')
        return redirect(url_for('home'))

    goal_id = request.form['goal_id']

    try:
        conn = get_db()
        cursor = conn.cursor()

        # Delete the savings goal from the database
        cursor.execute("DELETE FROM SAVINGS_GOAL_TRACKER WHERE id = %s AND username = %s", (goal_id, session['username']))
        conn.commit()
        
        flash('Savings goal deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting savings goal: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('view_goals'))

if __name__ == '__main__':
    app.run(debug=True)
