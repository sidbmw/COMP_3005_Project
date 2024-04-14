# Import necessary libraries
import psycopg2
import PySimpleGUI as sg
import re  # For email validation
from db_config import get_db_connection  # Import centralized database connection

# Connect to the database
con = get_db_connection()
cur = con.cursor()

# Function to run the member registration process
def run_member_registration():
    # Predefined fitness goals
    fitness_goals = ['Lose weight', 'Gain muscle', 'Improve stamina', 'Increase flexibility']
    
    # Define the layout for the registration form
    layout = [
        [sg.Text('Member Registration', size=(30, 1), justification='center', font=("Helvetica", 25))],
        [sg.Text('Name:', size=(15, 1)), sg.InputText()],
        [sg.Text('Email:', size=(15, 1)), sg.InputText()],
        [sg.Text('Password:', size=(15, 1)), sg.InputText(password_char='*')],  # Added password field
        [sg.Text('Fitness Goal:', size=(15, 1)), sg.Combo(fitness_goals, default_value=fitness_goals[0])],
        [sg.Text('Health Metrics:', size=(15, 1)), sg.InputText(), sg.Text('Example: BMI:25, Body Fat:20%')],
        [sg.Submit(), sg.Cancel()]
    ]
    
    # Create the window
    window = sg.Window('Register New Member', layout)
    
    # Function to validate email format
    def validate_email(email):
        pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        return re.match(pattern, email, re.I)

    # Function to validate fitness goal and health metrics
    def validate_fitness_goal(goal):
        # Accepting any predefined fitness goals from the dropdown menu
        if goal in fitness_goals:
            return True
        else:
            return False

    def validate_health_metrics(metrics):
        # Implementing specific validation for health metrics
        # Example: Metrics must include BMI or body fat percentage in a valid format
        pattern = r'^BMI:\s?\d+(\.\d+)?\s?,\s?Body Fat:\s?\d+(\.\d+)?%$'
        return re.match(pattern, metrics, re.I)

    # Event loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            break
        elif event == 'Submit':
            # Extract values
            name, email, password, fitness_goal, health_metrics = values[0], values[1], values[2], values[3], values[4]
            
            # Perform validations
            if not validate_email(email):
                sg.Popup('Invalid email format. Please enter a valid email.')
                continue
            if not validate_fitness_goal(fitness_goal):
                sg.Popup('Invalid fitness goal. Please enter a valid goal.')
                continue
            if not validate_health_metrics(health_metrics):
                sg.Popup('Invalid health metrics. Please enter valid metrics.')
                continue
            
            # Database insertion logic
            try:
                # Assuming a table named 'USERS' with columns 'USER_ID', 'USERNAME', 'PASSWORD', 'EMAIL', 'ROLE'
                # and a table named 'MEMBERS' with columns 'MEMBER_ID', 'USER_ID', 'FITNESS_GOAL', 'HEALTH_METRICS'
                cur.execute("""
                    INSERT INTO USERS (USERNAME, PASSWORD, EMAIL, ROLE)
                    VALUES (%s, %s, %s, 'member') RETURNING USER_ID""",
                    (name, password, email)
                )
                user_id = cur.fetchone()[0]
                cur.execute("""
                    INSERT INTO MEMBERS (USER_ID, NAME, FITNESS_GOAL, HEALTH_METRICS)
                    VALUES (%s, %s, %s, %s)""",
                    (user_id, name, fitness_goal, health_metrics)
                )
                con.commit()
                sg.Popup('Member registration successful.')
                window.close()  # Close the registration window
            except psycopg2.DatabaseError as e:
                print('Database error:', e)
    
    window.close()
# Function to run the main window (assuming this function exists)
def run_main_window():
    # Define the layout for the main window
    layout = [
        # Layout elements for the main window
    ]
    
    # Create and display the main window
    window = sg.Window('Main Window', layout).read(close=True)
