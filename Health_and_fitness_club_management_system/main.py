import psycopg2
import PySimpleGUI as sg
from db_config import get_db_connection
from Member_Registration import run_member_registration
from Profile_Management import update_member_profile  # Assuming this function is defined in Profile_Management.py

def verify_login(username, password):
    # Function to verify user login credentials against the database and return user role
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    if user:
        return True, user[2]  # Assuming 'role' is at index 2 in the tuple returned from the database
    else:
        return False, None

def open_user_dashboard(username):
    # Expanded function to open the user's dashboard and retrieve relevant information
    con = get_db_connection()
    cur = con.cursor()
    # Fetching member's fitness goals and health metrics based on their username
    cur.execute("SELECT m.fitness_goal, m.health_metrics FROM members m JOIN users u ON m.user_id = u.user_id WHERE u.username = %s", (username,))
    member_info = cur.fetchone()
    if member_info:
        fitness_goals, health_metrics = member_info
        sg.Popup("Dashboard", f"Welcome to your dashboard, {username}!\nFitness Goals: {fitness_goals}\nHealth Metrics: {health_metrics}")
    else:
        sg.Popup("Dashboard", "Dashboard information not available.")

    # Fetching trainer's upcoming training sessions
    cur.execute("SELECT s.start_time, s.end_time FROM schedule s JOIN users u ON s.trainer_id = u.user_id WHERE u.username = %s", (username,))
    sessions_info = cur.fetchall()
    if sessions_info:
        sessions_details = "\n".join([f"Start Time: {session[0]}, End Time: {session[1]}" for session in sessions_info])
        sg.Popup("Trainer Dashboard", f"Upcoming Training Sessions:\n{sessions_details}")
    else:
        sg.Popup("Trainer Dashboard", "No upcoming training sessions.")

    # Implementing dashboard display for admin staff showing room booking statuses
    cur.execute("SELECT room_id FROM booking")
    room_bookings = cur.fetchall()
    booking_details = "\n".join([f"Room ID: {booking[0]}" for booking in room_bookings])
    sg.Popup("Admin Dashboard", f"Room Booking Statuses:\n{booking_details}")

def main():
    # Attempt to connect to the database
    try:
        con = get_db_connection()
        print("Connected to the database successfully")
    except psycopg2.DatabaseError as e:
        sg.Popup("Database Connection Error", f"An error occurred while connecting to the database: {e}")
        return

    # Initial user interface layout
    layout = [
        [sg.Text('Welcome to the Health and Fitness Club Management System', size=(30, 2), justification='center', font=("Helvetica", 16))],
        [sg.Button('Login'), sg.Button('Register'), sg.Button('Update Profile'), sg.Button('Exit')]  # Added 'Update Profile' button
    ]
    
    window = sg.Window('Main Menu', layout)
    
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event == 'Login':
            # Open the login form and process login
            con = get_db_connection()
            cur = con.cursor()
            cur.execute("SELECT username FROM users")
            usernames = cur.fetchall()
            username_list = [user[0] for user in usernames]  # Extract usernames from the query result
            layout = [
                [sg.Text('Username'), sg.Combo(username_list)],
                [sg.Text('Password'), sg.InputText(password_char='*')],
                [sg.Button('Submit'), sg.Button('Cancel')]
            ]
            login_window = sg.Window('Login', layout)
            event, values = login_window.read()
            if event == 'Submit':
                username, password = values[0], values[1]
                login_success, user_role = verify_login(username, password)  # This function verifies credentials and returns user role
                if login_success:  # Open the user's dashboard upon successful login
                    open_user_dashboard(username)  
                else:
                    sg.Popup("Login Failed", "Invalid username or password.")
            login_window.close()
        elif event == 'Register':
            # Open the registration form
            run_member_registration()  # Assuming this function is defined in Member_Registration.py
        elif event == 'Update Profile':
            # Open the profile update form
            update_member_profile()  # Assuming this function is defined in Profile_Management.py
    
    window.close()

if __name__ == "__main__":
    main()
