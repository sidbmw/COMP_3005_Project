import psycopg2
import PySimpleGUI as sg
import re  # For email validation
from db_config import get_db_connection  

# Connect to the database
con = get_db_connection()
cur = con.cursor()

# Update member profile
def update_member_profile(member_id):
    # Fetch current member data
    cur.execute("SELECT m.name, u.email, m.fitness_goal, m.health_metrics FROM members m JOIN users u ON m.user_id = u.user_id WHERE m.member_id = %s", (member_id,))
    member_data = cur.fetchone()

    if member_data:
        # Layout for profile update form
        layout = [
            [sg.Text('Update Member Profile', size=(30, 1), justification='center', font=("Helvetica", 25))],
            [sg.Text('Name:', size=(15, 1)), sg.InputText(member_data[0])],
            [sg.Text('Email:', size=(15, 1)), sg.InputText(member_data[1], key='email')],
                       [sg.Text('Fitness Goal:', size=(15, 1)), sg.Combo(['Lose Weight', 'Gain Muscle', 'Improve Stamina'], default_value=member_data[2], key='fitness_goal')],
            [sg.Text('Health Metrics:', size=(15, 1)), sg.InputText(member_data[3], key='health_metrics')],
            [sg.Submit(), sg.Cancel()]
        ]

        # Create window for profile update
        window = sg.Window('Update Profile', layout)

        # Event loop for form actions
        while True:
            event, values = window.read()
            if event in (None, 'Cancel'):
                window.close()
                break
            elif event == 'Submit':
                # Update member data in database
                try:
                    cur.execute("UPDATE MEMBERS SET FITNESS_GOAL = %s, HEALTH_METRICS = %s WHERE MEMBER_ID = %s", (values['fitness_goal'], values['health_metrics'], member_id))
                    cur.execute("UPDATE USERS SET EMAIL = %s WHERE USER_ID = %s", (values['email'], member_id))
                    con.commit()
                    sg.Popup('Profile update successful.')
                    window.close()
                    break
                except psycopg2.DatabaseError as e:
                    print(f"Database error: {e}")  # Handle database error
                    sg.Popup('Database error:', e)

    else:
        sg.Popup('Member not found.')

# Placeholder for the main function that shows the main menu
def main():
    # Main menu code here
    pass
