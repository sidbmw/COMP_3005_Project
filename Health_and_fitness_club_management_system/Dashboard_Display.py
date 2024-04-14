# Import necessary libraries
import psycopg2
import PySimpleGUI as sg
from db_config import get_db_connection

# Connect to the database
con = get_db_connection()
cur = con.cursor()

# Function to display the member's dashboard
def display_member_dashboard():
    # Placeholder for member ID input
    member_id = sg.popup_get_text('Enter Member ID')
    
    # Implement data retrieval logic
    cur.execute("SELECT exercise_routines, fitness_achievements, health_statistics FROM members WHERE member_id = %s", (member_id,))
    data = cur.fetchone()
    exercise_routines, fitness_achievements, health_statistics = data if data else ("No data", "No data", "No data")
    
    # Updated GUI layout for the dashboard to display real data
    layout = [
        [sg.Text('Member Dashboard', size=(30, 1), justification='center', font=("Helvetica", 25))],
        [sg.Text('Exercise Routines:'), sg.Multiline(exercise_routines, size=(35, 5))],
        [sg.Text('Fitness Achievements:'), sg.Multiline(fitness_achievements, size=(35, 5))],
        [sg.Text('Health Statistics:'), sg.Multiline(health_statistics, size=(35, 5))],
        [sg.Button('Close')]
    ]
    
    # Create the window
    window = sg.Window('Member Dashboard', layout)
    
    # Event loop to process "events"
    while True:
        event, values = window.read()
        if event in (None, 'Close'):
            break
    
    window.close()

# Placeholder for member ID input removed and function call updated
display_member_dashboard()
