# Import required libraries.
import psycopg2
import PySimpleGUI as sg
from db_config import get_db_connection

# Connect to the database.
con = get_db_connection()
cur = con.cursor()

# Function to show the member's dashboard.
def display_member_dashboard(member_id):
    print("Displaying member dashboard for member_id: %s" % member_id)  # Log the display action.
    
    # Retrieve exercise routines.
    cur.execute("SELECT routine_details FROM exercise_routines WHERE member_id = %s", (member_id,))
    routines_data = cur.fetchone()
    exercise_routines = routines_data if routines_data else "No data"
    print("Fetched exercise routines: %s" % exercise_routines)  # Log retrieved exercise routines.
    
    # Retrieve fitness achievements.
    cur.execute("SELECT achievement_details FROM fitness_achievements WHERE member_id = %s", (member_id,))
    achievements_data = cur.fetchone()
    fitness_achievements = achievements_data if achievements_data else "No data"
    print("Fetched fitness achievements: %s" % fitness_achievements)  # Log retrieved fitness achievements.
    
    # Assume health statistics are fetched separately.
    health_statistics = "Sample health statistics data"
    print("Health Statistics: %s" % health_statistics)  # Log health statistics.
    
    # Set up the GUI layout for the dashboard.
    layout = [
        [sg.Text('Member Dashboard', size=(30, 1), justification='center', font=("Helvetica", 25))],
        [sg.Text('Exercise Routines:'), sg.Multiline(exercise_routines, size=(35, 5))],
        [sg.Text('Fitness Achievements:'), sg.Multiline(fitness_achievements, size=(35, 5))],
        [sg.Text('Health Statistics:'), sg.Multiline(health_statistics, size=(35, 5))],
        [sg.Button('Close')]
    ]
    
    # Initialize the window.
    window = sg.Window('Member Dashboard', layout)
    
    # Handle window events.
    while True:
        event, values = window.read()
        if event in (None, 'Close'):
            break
    print("Dashboard displayed successfully")  # Log dashboard display.
    
    window.close()
