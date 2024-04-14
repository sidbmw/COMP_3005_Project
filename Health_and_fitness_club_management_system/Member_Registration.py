import psycopg2
import PySimpleGUI as sg
import re  
from db_config import get_db_connection  

# Connect to the database
con = get_db_connection()
cur = con.cursor()

# Run the member registration process
def run_member_registration():
    # Define fitness goals
    fitness_goals = ['Lose weight', 'Gain muscle', 'Improve stamina', 'Increase flexibility']
    
    # Layout for the registration form
    layout = [
        [sg.Text('Member Registration', size=(30, 1), justification='center', font=("Helvetica", 25))],
        [sg.Text('Name:', size=(15, 1)), sg.InputText()],
        [sg.Text('Email:', size=(15, 1)), sg.InputText()],
        [sg.Text('Password:', size=(15, 1)), sg.InputText(password_char='*')],
        [sg.Text('Fitness Goal:', size=(15, 1)), sg.Combo(fitness_goals, default_value=fitness_goals[0])],
        [sg.Text('Health Metrics:', size=(15, 1)), sg.InputText(), sg.Text('Example: BMI:25, Body Fat:20%')],
        [sg.Submit(), sg.Cancel()]
    ]
    
    # Create the registration window
    window = sg.Window('Register New Member', layout)
    
    # Validate email format
    def validate_email(email):
        pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        return re.match(pattern, email, re.I)

    # Validate fitness goal
    def validate_fitness_goal(goal):
        if goal in fitness_goals:
            return True
        else:
            return False

    # Validate health metrics
    def validate_health_metrics(metrics):
        pattern = r'^BMI:\s?\d+(\.\d+)?\s?,\s?Body Fat:\s?\d+(\.\d+)?%$'
        return re.match(pattern, metrics, re.I)

    # Event loop for form actions
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            break
        elif event == 'Submit':
            # Extract values
            name, email, password, fitness_goal, health_metrics = values[0], values[1], values[2], values[3], values[4]
            
            # Validate form inputs
            if not validate_email(email):
                sg.Popup('Invalid email format. Please enter a valid email.')
                continue
            if not validate_fitness_goal(fitness_goal):
                sg.Popup('Invalid fitness goal. Please enter a valid goal.')
                continue
            if not validate_health_metrics(health_metrics):
                sg.Popup('Invalid health metrics. Please enter valid metrics.')
                continue
            
            # Insert data into the database
            try:
                cur.execute("INSERT INTO USERS (USERNAME, PASSWORD, EMAIL, ROLE) VALUES (%s, %s, %s, 'member') RETURNING USER_ID", (name, password, email))
                user_id = cur.fetchone()[0]
                cur.execute("INSERT INTO MEMBERS (USER_ID, NAME, FITNESS_GOAL, HEALTH_METRICS) VALUES (%s, %s, %s, %s)", (user_id, name, fitness_goal, health_metrics))
                con.commit()
                sg.Popup('Member registration successful.')
                window.close()
            except psycopg2.DatabaseError as e:
                print('Database error:', e)
