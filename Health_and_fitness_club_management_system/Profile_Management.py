# Import necessary libraries
import psycopg2
import PySimpleGUI as sg
import re  # For email validation
from db_config import get_db_connection

# Connect to the database
con = get_db_connection()
cur = con.cursor()

# Function to fetch and update member profile
def update_member_profile():
    # Fetching usernames for the dropdown
    cur.execute("SELECT username FROM users")
    usernames = cur.fetchall()
    usernames_list = [username[0] for username in usernames]  # Convert tuple list to a list of usernames
    
    # Replacing with dropdown for username selection
    layout = [
        [sg.Text('Select your username')],
        [sg.Combo(usernames_list, key='username_selected')],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]
    
    window = sg.Window('Select Username', layout)
    
    event, values = window.read()
    window.close()
    
    if event == 'Submit':
        username_selected = values['username_selected']
        
        # Fetch member ID based on selected username
        cur.execute("SELECT id FROM users WHERE username = %s", (username_selected,))
        member_id_row = cur.fetchone()
        member_id = member_id_row[0] if member_id_row else None
        
        if not member_id:
            sg.Popup("Username not found.")
            return
        
        # Fetch current member data from the database
        cur.execute("SELECT NAME, EMAIL, FITNESS_GOAL, HEALTH_METRICS FROM MEMBERS WHERE MEMBER_ID = %s", (member_id,))
        member_data = cur.fetchone()
        
        if member_data:
            # Define the layout for the profile update form
            layout = [
                [sg.Text('Update Member Profile', size=(30, 1), justification='center', font=("Helvetica", 25))],
                [sg.Text('Name:', size=(15, 1)), sg.InputText(member_data[0])],
                [sg.Text('Email:', size=(15, 1)), sg.InputText(member_data[1])],
                [sg.Text('Fitness Goal:', size=(15, 1)), sg.InputText(member_data[2])],
                [sg.Text('Health Metrics:', size=(15, 1)), sg.InputText(member_data[3])],
                [sg.Submit(), sg.Cancel()]
            ]
            
            # Create the window
            window = sg.Window('Update Profile', layout)
            
            # Event loop to process "events" and get the "values" of the inputs
            while True:
                event, values = window.read()
                if event in (None, 'Cancel'):
                    break
                elif event == 'Submit':
                    # Update member data in the database
                    try:
                        # Implementing specific validation for fitness goals
                        # Example: Goal must be a numeric value followed by "kg" for weight or "weeks" for time-based goals
                        pattern_goal = r'^\d+(\.\d+)?\s?(kg|weeks)$'
                        # Implementing specific validation for health metrics
                        # Example: Metrics must include BMI or body fat percentage in a valid format
                        pattern_metrics = r'^BMI:\s?\d+(\.\d+)?\s?,\s?Body Fat:\s?\d+(\.\d+)?%$'
                        if not re.match(pattern_goal, values[2], re.I):
                            sg.Popup('Invalid fitness goal format. Please use "kg" for weight or "weeks" for time-based goals.')
                            continue
                        if not re.match(pattern_metrics, values[3], re.I):
                            sg.Popup('Invalid health metrics format. Please use "BMI: [value], Body Fat: [percentage]%".')
                            continue
                        cur.execute("""
                            UPDATE MEMBERS
                            SET NAME = %s, EMAIL = %s, FITNESS_GOAL = %s, HEALTH_METRICS = %s
                            WHERE MEMBER_ID = %s""",
                            (values[0], values[1], values[2], values[3], member_id)
                        )
                        con.commit()
                        sg.Popup('Profile update successful.')
                    except psycopg2.DatabaseError as e:
                        sg.Popup('Database error:', e)
            
            window.close()
        else:
            sg.Popup('Member not found.')

