import psycopg2
import PySimpleGUI as sg
from db_config import get_db_connection
from Member_Registration import run_member_registration
from Profile_Management import update_member_profile  
from Dashboard_Display import display_member_dashboard  
from Trainer_Schedule_Management import schedule_session  
from Trainer_Schedule_Management import view_scheduled_sessions  

def verify_login(username, password):
    # Verify user login credentials.
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    if user:
        return True, user[2]  
    else:
        return False, None

def open_user_dashboard(username):
    # Open the user's dashboard.
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

    # Fetch trainer's upcoming sessions.
    cur.execute("SELECT s.start_time, s.end_time FROM schedule s JOIN users u ON s.trainer_id = u.user_id WHERE u.username = %s", (username,))
    sessions_info = cur.fetchall()
    if sessions_info:
        sessions_details = "\n".join([f"Start Time: {session[0]}, End Time: {session[1]}" for session in sessions_info])
        sg.Popup("Trainer Dashboard", f"Upcoming Training Sessions:\n{sessions_details}")
    else:
        sg.Popup("Trainer Dashboard", "No upcoming training sessions.")

    # Display admin dashboard with room bookings.
    cur.execute("SELECT room_id FROM booking")
    room_bookings = cur.fetchall()
    booking_details = "\n".join([f"Room ID: {booking[0]}" for booking in room_bookings])
    sg.Popup("Admin Dashboard", f"Room Booking Statuses:\n{booking_details}")

def main():
    # Main function to start the application.
    try:
        con = get_db_connection()
        print("Connected to the database successfully")
    except psycopg2.DatabaseError as e:
        sg.Popup("Database Connection Error", f"An error occurred while connecting to the database: {e}")
        return

    # Set up the initial UI layout.
    layout = [
        [sg.Text('Welcome to the Health and Fitness Club Management System', size=(30, 2), justification='center', font=("Helvetica", 16))],
        [sg.Button('Login'), sg.Button('Register'), sg.Button('Update Profile'), sg.Button('Schedule Management'), sg.Button('View Sessions'), sg.Button('Exit')]  # Added 'View Sessions' button
    ]
    
    window = sg.Window('Main Menu', layout)
    
    # Track the logged-in user's ID and role.
    logged_in_user_id = None
    logged_in_user_role = None
    
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
                    # Fetch the correct member_id based on the username
                    cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                    user_id_result = cur.fetchone()
                    if user_id_result:
                        logged_in_user_id = user_id_result[0]
                        logged_in_user_role = user_role
                        sg.Popup("Login Successful", f"Welcome, {username}!")
                    else:
                        sg.Popup("Error", "Member ID not found.")
                else:
                    sg.Popup("Login Failed", "Invalid username or password.")
            login_window.close()
        elif event == 'Register':
            # Open the registration form
            run_member_registration()  
        elif event == 'Update Profile':
            # Open the profile update form
            if logged_in_user_id:
                update_member_profile(logged_in_user_id)  
            else:
                sg.Popup("Error", "Please log in to update your profile.")
        elif event == 'Schedule Management':
            # Check if user is logged in before accessing Schedule Management
            if logged_in_user_id:
                # Allow the user to specify the session_type and other details before calling schedule_session()
                layout = [
                    [sg.Text('Select Session Type:'), sg.Combo(['Personal Training', 'Group Fitness Class'], key='session_type')],
                    [sg.Text('Trainer ID:'), sg.InputText(key='trainer_id')],
                    [sg.Text('Start Time (YYYY-MM-DD HH:MM):'), sg.InputText(key='start_time')],
                    [sg.Text('End Time (YYYY-MM-DD HH:MM):'), sg.InputText(key='end_time')],
                    [sg.Button('Submit'), sg.Button('Cancel')]
                ]
                session_window = sg.Window('Schedule Session', layout)
                event, values = session_window.read()
                if event == 'Submit':
                    session_type = values['session_type']
                    trainer_id = values['trainer_id']
                    start_time = values['start_time']
                    end_time = values['end_time']
                    if session_type == 'Personal Training':
                        # Call the function to schedule a personal training session with all required parameters
                        schedule_session(logged_in_user_id, 'personal_training', trainer_id, None, start_time, end_time)
                        sg.Popup("Success", "Personal Training session scheduled.")
                    elif session_type == 'Group Fitness Class':
                        # Call the function to register for a group fitness class with required parameters
                        schedule_session(logged_in_user_id, 'group_fitness', None, None, start_time, end_time)
                        sg.Popup("Success", "Registered for Group Fitness Class.")
                session_window.close()
            else:
                sg.Popup("Error", "Please log in to manage your schedule.")
        elif event == 'View Sessions':
            # Check if user is logged in before viewing sessions
            if logged_in_user_id:
                # Call the function to view scheduled sessions for the logged-in member
                session_info = view_scheduled_sessions(logged_in_user_id)
                if session_info:  # Check if there are any sessions to display
                    sessions_details = "\n".join([f"Session Type: {session['type']}, Trainer: {session['trainer']}, Start: {session['start_time']}, End: {session['end_time']}" for session in session_info])
                    sg.Popup("Your Scheduled Sessions", sessions_details)
                else:
                    sg.Popup("No Scheduled Sessions", "You have no scheduled sessions.")
            else:
                sg.Popup("Error", "Please log in to view your sessions.")
    
    window.close()

if __name__ == "__main__":
    main()
