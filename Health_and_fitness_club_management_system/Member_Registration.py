# Import necessary libraries
import psycopg2
import PySimpleGUI as sg
import re  # Additional imports for validation

# Function to run the member registration process
def run_member_registration():
    # Connect to the database
    con = psycopg2.connect(
        dbname='your_dbname',
        user='your_username',
        password='your_password',
        host='localhost'
    )
    cur = con.cursor()
    
    # Define the layout for the registration form
    layout = [
        [sg.Text('Member Registration', size=(30, 1), justification='center', font=("Helvetica", 25))],
        [sg.Text('Name:', size=(15, 1)), sg.InputText()],
        [sg.Text('Email:', size=(15, 1)), sg.InputText()],
        [sg.Text('Fitness Goal:', size=(15, 1)), sg.InputText()],
        [sg.Text('Health Metrics:', size=(15, 1)), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]
    
    # Create the window
    window = sg.Window('Register New Member', layout)
    
    # Function to validate email format
    def validate_email(email):
        pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        return re.match(pattern, email, re.I)

    # Function to validate fitness goal and health metrics (placeholder for actual validation logic)
    def validate_fitness_goal(goal):
        # Implementing specific validation for fitness goals
        # Example: Goal must be a numeric value followed by "kg" for weight or "weeks" for time-based goals
        pattern = r'^\d+(\.\d+)?\s?(kg|weeks)$'
        return re.match(pattern, goal, re.I)

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
            name, email, fitness_goal, health_metrics = values[0], values[1], values[2], values[3]
            
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
            
            # Placeholder for database insertion logic
            try:
                # Assuming a table named 'MEMBERS' with columns 'NAME', 'EMAIL', 'FITNESS_GOAL', 'HEALTH_METRICS'
                cur.execute("""
                    INSERT INTO MEMBERS (NAME, EMAIL, FITNESS_GOAL, HEALTH_METRICS)
                    VALUES (%s, %s, %s, %s)""",
                    (name, email, fitness_goal, health_metrics)
                )
                con.commit()
                sg.Popup('Member registration successful.')
            except psycopg2.DatabaseError as e:
                sg.Popup('Database error:', e)
    
    window.close()

# Call the function to run the program
if __name__ == '__main__':
    run_member_registration()
