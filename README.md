# SmartSaver-Budget Smart, Live Better

## Overview

SmartSaver is a budget forecasting application designed to help users manage their finances efficiently. By allowing users to input their income and expenses, the app forecasts monthly budgets, sets savings goals, and predicts the time required to achieve these goals based on disposable income allocation. It also provides the insights of the user's expenses and income.

---
## System Requirements

### Software
- Operating System: Windows, macOs.
- Python 3.8 or higher
- Snowflake account

### Libraries and Tools
-  Flask (latest stable version)
-  Chart.js (for data visualization)
-  Snowflake Connector
-  datetime for date conversions
---
## Installations

### Prerequisites
Before you begin, ensure you have met the following requirements:
- You have a Windows, macOS operating sytem.
- You have installed Python 3.8 or higher.
- You have an active snowflake account.

### Step-by-Step Installation Guide

#### 1. Clone the Repository

git clone 
cd smartsaver

#### 2. Configure Snowflake
1. Create snowflake account at https://www.snowflake.com/en/
2. Install Snowflake connector for Python in command prompt:
  **pip install snowflake-connector-python**
   
#### 3. Replace Snowflake credentials:
Replace your own snowflake credentials in app.py

#### 4. Run the Application:
1. Execute application with command ***python3 app.py**

#### 5. Access the Application:
Open your web browser and navigate to http://127.0.0.1:5000/ to access the SmartSaver application.

## Additional Notes

Execute all the DDL statements of associated tables in Snowflake UI

---
## Usage
### Authentication:

1.Enter username and password to login.
2. If you don't have account, register using the registration link by providing required details such as Name, Email etc..

### Set Savings Goals:

1. Navigate to the "Set Savings Goals" section.
2. Enter your monthly disposable income, savings goal item, savings goal amount, and allocation percentage.
3. Click "Save Goal" to save your goal.

### View Savings Goals:

1. Navigate to the "View Savings Goals" section.
2. View your saved goals along with details such as item, amount, allocation percentage, monthly income, created date, and the forecasted end date for achieving the goal.

### Visualizing Data:

1. Select "Income" or "Expense" from the dropdown to visualize data.
2. The chart will update to show your income or expense data over time.

### Adding Income or Expense:

1. Choose "Expense" or "Income" from the dropdown menu.
2. Fill in the frequency, type, notes, and amount for the income or expense.
3. Click the "Submit" button to save your data.

By following these steps, you can effectively manage and visualize your financial data using SmartSaver.



## Key Features

- **Monthly Budget Forecasting:** Forecast monthly budgets using income and expenses data.
- **Frequency Specification:** Specify income and expense frequency (weekly, bi-weekly, monthly, etc.).
- **Data Retention:** Persist user data across sessions for continuous access.
- **Security:** Securely store and encrypt user budget data.
- **Savings Goals:** Set and track savings goals, e.g., for a house down payment.
- **Goal Forecasting:** Predict time required to achieve savings goals based on allocated income percentage.

---

## Additional Features

- **Expense Comparison:** Compare expenses between previous and current months.
- **Expense Graph:** Visualize expenditure trends with graphs.

---


### Contact
Contact below team members for the respective scoping of the project.
- **Responsibilities by Team Members:**
  - **Abhi Stephen Rokkam:** Focus on core functionalities.
  - **Navya Chowdary Nelluri:** Define sprint deliverables.
  - **Mounika Bireddy:** Peer review and quality assurance.
  - **Krishna Reddy Syamala:** Evaluate deliverable complexity.

