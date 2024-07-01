# High-Level Design Document for SmartSaver

## Introduction

SmartSaver is a Flask-based application designed to help users manage and forecast their monthly budgets. The system allows users to input their income and expenses, set savings goals, and forecast the time required to achieve these goals based on their disposable income.

## Main Components

### User Interface (UI)
- **Technology:** HTML, CSS, JavaScript
- **Functionality:** Provides an interface for users to input data (income, expenses, savings goals), view forecasts, and manage their budgets.
- **Pages:**
  - `dashboard.html`
    *:* Main interface displaying an overview of the user's financial status with key metrics and visualizations.
  - `home.html`
    *:* Landing page introducing the SmartSaver app with navigation links to other sections.
  - `login.html`
    *:* User authentication page with fields for email and password.
  - `register.html`
    *:* New user registration page collecting name, email, and password.
  - `savinggoals.html`
    *:* Interface for users to set and manage new savings goals.
  - `viewgoals.html`
    *:* Displays user's existing savings goals with details and options to edit or delete.
    
### Backend Server
- **Technology:** Flask (Python)
- **Functionality:** Handles user requests, processes data, interacts with the database, and communicates with external services for data storage and processing.

### Database
- **Technology:** Snowflake
- **Functionality:** Stores user data, including income, expenses, and savings goals. Provides query capabilities for forecasting and data retrieval.

## Scope of the Project

The SmartSaver project aims to provide users with a robust platform for managing and forecasting their monthly budgets effectively. Users can input their income and expenses, set specific savings goals, and track their progress towards achieving them. The application supports various functionalities such as user authentication, registration, and interactive interfaces for data input and visualization. Key features include a dashboard for real-time financial status updates, comprehensive views of income and expenses, and tools to forecast the time needed to reach savings goals based on allocated percentages of disposable income. The system offers a seamless user experience across different devices and operating systems. SmartSaver empowers users to make informed financial decisions by providing clear insights into their spending patterns and savings progress, ultimately promoting better financial management and goal attainment.

## Architecture Diagram
---
<img src="static/Architecture.jpg" alt="Diagram" width="800" height="600">

The architecture consists of a client-server model with the following flow:

1. **User Interaction:**
   - Users interact with the application through the UI.
   - The UI sends requests to the server based on user actions (e.g., submitting income data).

2. **Server Processing:**
   - The server processes incoming requests, interacts with the database, and returns the results to the UI.
   - The server also executes Python scripts for forecasting and data processing.

3. **Database Interaction:**
   - The server interacts with the Snowflake database to store and retrieve data.
   - The database handles queries for forecasting and confirms data insertions.

## ER Diagram
---
<img src="static/ERdiagram.jpg" alt="Diagram" width="800" height="600">

### Entities and Attributes

1. **USER:**
   - `id` (int, PK): Unique identifier for the user.
   - `name` (string): User's name.
   - `email` (string): User's email address.
   - `password` (string): User's password.

2. **INCOME:**
   - `id` (int, PK): Unique identifier for the income entry.
   - `user_id` (int, FK): References the user's `id`.
   - `amount` (float): Income amount.
   - `type` (string): Type of income.
   - `frequency` (string): Frequency of income.
   - `notes` (string): Additional notes.
   - `created_at` (date): Date of entry creation.

3. **EXPENSE:**
   - `id` (int, PK): Unique identifier for the expense entry.
   - `user_id` (int, FK): References the user's `id`.
   - `amount` (float): Expense amount.
   - `type` (string): Type of expense.
   - `frequency` (string): Frequency of expense.
   - `notes` (string): Additional notes.
   - `created_at` (date): Date of entry creation.

4. **SAVINGS_GOAL:**
   - `id` (int, PK): Unique identifier for the savings goal.
   - `user_id` (int, FK): References the user's `id`.
   - `item` (string): Item for the savings goal.
   - `goal_amount` (float): Target amount.
   - `allocation_percentage` (float): Percentage of disposable income allocated.
   - `monthly_income` (float): Monthly disposable income.
   - `created_at` (date): Date of goal creation.
   - `forecasted_end_date` (date): Estimated date to achieve the goal.

## Sequence Diagram
---
<img src="static/sequenceDiagram.jpg" alt="Diagram" width="800" height="600">

### Sequence of Actions

1. *User Actions:*
   - Requests forecast data.
   - Enters savings goal details, expense details, and income details.

2. *UI Actions:*
   - Sends forecast request to the server.
   - Submits savings goal, expense data, and income data.

3. *Server Actions:*
   - Processes requests, interacts with Python scripts, and communicates with Snowflake.
   - Returns forecast data and confirmation messages to the UI.

4. *Python Script Actions:*
   - Processes data and interacts with Snowflake for data storage and retrieval.
   - Returns processed data and confirmation messages to the server.

5. *Snowflake Actions:*
   - Handles queries and data insertion.
   - Confirms data insertion and returns queried data.

## Conclusion

This high-level design document provides an overview of the SmartSaver application's architecture, including the main components, their interactions, and detailed diagrams. This document will evolve as the project progresses, incorporating additional details and refinements. The accompanying README.md ensures that users and developers can easily set up and understand the project.
